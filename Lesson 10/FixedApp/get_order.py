import json
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    print(json.dumps(event))
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o) if o % 1 else int(o)
            return super().default(o)

   #Fixed the code to handle both admin and non-admin users correctly when fetching order details from DynamoDB. Admin users can query by orderId, while non-admin users must provide both orderId and userId to ensure they only access their own orders.
    try:
        orderId = event.get("orderId")
        userId = event.get("user")
        is_admin = event.get("isAdmin", False)

        if not orderId or not userId:
            raise KeyError

    except KeyError:
        return {"status": "err", "msg": "Missing required fields"}

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["ORDERS_TABLE"])

 #Fixed the code to handle both admin and non-admin users correctly when fetching order details from DynamoDB. Admin users can query by orderId, while non-admin users must provide both orderId and userId to ensure they only access their own orders.
    try:
        if is_admin:
            result = table.query(
                KeyConditionExpression=Key("orderId").eq(orderId)
            )
            items = result.get("Items", [])
            order = items[0] if items else None

        else:
            key = {"orderId": orderId, "userId": userId}
            order = table.get_item(Key=key).get("Item")

    except Exception as e:
        print("DynamoDB error:", str(e))
        return {"status": "err", "msg": "Database error"}

    
    if not order:
        return {"status": "err", "msg": "could not find order"}

    res = {"status": "ok", "order": order}

    return json.loads(json.dumps(res, cls=DecimalEncoder)) 
