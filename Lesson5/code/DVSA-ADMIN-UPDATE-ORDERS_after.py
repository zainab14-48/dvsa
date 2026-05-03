token = json.loads(auth_data)
user = token["username"]

if "role" not in token or token["role"] != "admin":
    return {"status": "err", "msg": "Unauthorized"}

action = event['body']['action']
orderId = event['body']['order-id']
item = event['body']['item']
ts = int(time.time())
