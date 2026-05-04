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

    try:
        response = table.update_item(
            Key=key,
            UpdateExpression="SET itemList = :itemList",
            ExpressionAttributeValues={
                ":itemList": itemList
            }
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return {"status": "ok", "msg": "cart updated"}

        return {"status": "err", "msg": "could not update cart"}

    except Exception as e:
        print("Update error:", str(e))
        return {
            "status": "err",
            "msg": "order could not be updated",
            "error": str(e)
        }