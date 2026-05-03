import json
import boto3
import os

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

    orderId = event["orderId"]
    itemList = event["items"]
    userId = event["user"]

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])

    key = {
        "orderId": orderId,
        "userId": userId
    }

    response = table.get_item(
        Key=key,
        AttributesToGet=["orderStatus"]
    )

    if "Item" not in response:
        return {"status": "err", "msg": "could not find order"}

    current_status = int(response["Item"]["orderStatus"])

    # FIX 1: Block update after payment
    if current_status >= 120:
        return {"status": "err", "msg": "order already paid"}

    try:
        #  FIX 2(race condition fix)
        response = table.update_item(
            Key=key,
            UpdateExpression="SET itemList = :itemList",
            ConditionExpression="orderStatus < :paid",
            ExpressionAttributeValues={
                ":itemList": itemList,
                ":paid": 120
            }
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return {"status": "ok", "msg": "cart updated"}

        return {"status": "err", "msg": "could not update cart"}

    except Exception as e:
        print("Update error:", str(e))
        return {
            "status": "err",
            "msg": "order could not be updated; it may already be paid or locked",
            "error": str(e)
        }