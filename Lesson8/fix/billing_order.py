import json
import urllib3
import boto3
import os
import time
import decimal
from decimal import Decimal


# status list
# -----------
# 100: open
# 110: payment-failed
# 120: paid
# 200: processing
# 210: shipped
# 300: delivered
# 500: cancelled
# 600: rejected

def lambda_handler(event, context):
    print(json.dumps(event))

    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    orderId = event["orderId"]
    userId = event["user"]
    http = urllib3.PoolManager()

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])

    response = table.get_item(
        Key={
            "orderId": orderId,
            "userId": userId
        },
        AttributesToGet=["orderId", "orderStatus", "itemList"]
    )

    if "Item" not in response:
        return {"status": "err", "msg": "could not find order"}

    order = response["Item"]
    status = int(json.dumps(order["orderStatus"], cls=DecimalEncoder))

    if status >= 120:
        return {"status": "err", "msg": "order already made"}

    data_dict = []
    for key, value in order.get("itemList", {}).items():
        data_dict.append({
            "itemId": key,
            "quantity": int(value)
        })

    if not data_dict:
        return {"status": "err", "msg": "order has no items"}

    data = json.dumps(data_dict, cls=DecimalEncoder)

    # GET TOTAL FOR BILLING
    url = os.environ["GET_CART_TOTAL"]
    clen = len(data)

    req = http.request(
        "POST",
        url,
        body=data,
        headers={
            "Content-Type": "application/json",
            "Content-Length": str(clen)
        }
    )

    res = json.loads(req.data.decode("utf-8"))

    if not isinstance(res, dict) or "total" not in res:
        return {
            "status": "err",
            "msg": "cart total could not be calculated; order may have been modified during billing",
            "cart_total_response": res
        }

    cartTotal = float(res["total"])
    missings = res.get("missing", {})

    # SEND BILLING DATA TO PAYMENT
    url = os.environ["PAYMENT_PROCESS_URL"]
    data = json.dumps(event["billing"])
    clen = len(data)

    req = http.request(
        "POST",
        url,
        body=data,
        headers={
            "Content-Type": "application/json",
            "Content-Length": str(clen)
        }
    )

    res = json.loads(req.data.decode("utf-8"))
    ts = int(time.time())

    if res.get("status") == 110:
        return {"status": "err", "msg": "invalid payment details"}

    elif res.get("status") == 120:
        key = {
            "orderId": orderId,
            "userId": userId
        }

        update_expression = (
            "SET orderStatus = :orderstatus, "
            "paymentTS = :paymentTS, "
            "totalAmount = :total, "
            "confirmationToken = :token"
        )

        TWOPLACES = Decimal("0.01")

        expression_attributes = {
            ":orderstatus": res["status"],
            ":paymentTS": ts,
            ":total": Decimal(str(cartTotal)).quantize(TWOPLACES),
            ":token": res["confirmation_token"]
        }

        if missings:
            new_item_list = {}
            response = table.get_item(Key=key)
            items = response.get("Item", {}).get("itemList", {})

            for item in items:
                new_item_list[item] = items[item] - missings[item] if missings.get(item) else items[item]

            expression_attributes[":il"] = new_item_list
            update_expression += ", itemList = :il"

        try:
            table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attributes
            )

            sqs = boto3.client("sqs")
            sqs.send_message(
                QueueUrl=os.environ["SQS_URL"],
                MessageBody=json.dumps({
                    "orderId": orderId,
                    "userId": userId
                }),
                DelaySeconds=10
            )

            return {
                "status": "ok",
                "amount": float(cartTotal),
                "token": res["confirmation_token"],
                "missing": missings
            }

        except Exception as e:
            print("Update order error:", str(e))
            return {"status": "err", "msg": "unknown error"}

    else:
        return {"status": "err", "msg": "could not process payment"}