# Lesson 8 – Logic Vulnerability (Race Condition)

## 📌 Overview

This lesson demonstrates a **race condition vulnerability** in the DVSA order workflow.

The issue allows an attacker to modify an order **while the billing process is executing**, which may lead to inconsistent or incorrect order states.

---

## 🎯 Goal

Demonstrate that:

- Order updates can occur **during or after billing**
- The system does not enforce correct workflow sequencing
- This leads to **inconsistent payment and order data**

---

## ⚙️ Environment

- DVSA deployed on AWS using:
  - API Gateway
  - Lambda
  - DynamoDB
- Testing tools:
  - AWS CloudShell / terminal
  - `curl`
  - Browser DevTools
  - `jq`

---

## 🧪 Reproduction Steps — Vulnerable State

### 1. Create Order

```bash
curl -s "$API" \
-H "content-type: application/json" \
-H "authorization: $TOKEN" \
--data-raw '{"action":"new","cart-id":"lesson8-cart","items":{"1017":1}}'
```

Save the returned order ID:

```bash
export ORDER_ID="<ORDER_ID>"
```

---

### 2. Add Shipping

```bash
curl -s "$API" \
-H "content-type: application/json" \
-H "authorization: $TOKEN" \
--data-raw '{"action":"shipping","order-id":"<ORDER_ID>","data":{"address":"123 Test","email":"test@test.com","name":"Test"}}'
```

---

### 3. Run Race Condition Test

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

## ❗ Vulnerability Evidence

Observed output before the fix:

```json
{"status":"err","msg":"order already made"}
{"status":"ok","msg":"cart updated"}
```

This indicates that billing had already completed, but the cart update was still accepted.

---

## 🔍 Analysis

- Billing completed and the order was marked as paid.
- The update request still succeeded and changed the cart after payment.
- This violates the intended workflow rule:

```text
A paid order must not be modified.
```

---

## 🧠 Root Cause

The root cause was incomplete server-side workflow enforcement:

- No validation preventing updates after payment
- No synchronization between billing and update operations
- No atomic enforcement of order state in DynamoDB
- The application relied on normal request order instead of enforcing state transitions safely

---

## 🔐 Fix Strategy

Two-layer protection was implemented.

### 1. Logical Validation

The backend checks the order status before allowing cart or shipping updates.

```python
if current_status >= 120:
    return {"status": "err", "msg": "order already paid"}
```

Status `120` means the order is already paid.

---

### 2. Atomic Database Protection

A DynamoDB condition was added to prevent the update if the order was already paid.

```python
ConditionExpression="orderStatus < :paid"
```

This prevents race conditions even if two requests arrive at nearly the same time.

---

## 🛠️ Fixed Code — `update_order.py`

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

## ✅ Verification After Fix

After applying the fix, the race condition test was repeated.

Observed output after the fix:

```json
{"status":"ok","amount":45}
{"status":"err","msg":"order already paid"}
```

---

## ✔ Result

- Billing succeeds once.
- Update is rejected after payment.
- Order state remains consistent.
- The race condition is mitigated.

---

## 📸 Evidence

Screenshots included:

- `before_race.png` → vulnerable behavior
- `after_race.png` → fixed behavior
- `fix_code.png` → applied fix

---

## 🎯 Conclusion

The vulnerability allowed modification of orders during billing due to missing workflow validation and lack of atomic control.

After applying the fix:

- Order updates are blocked after payment.
- The race condition is mitigated.
- System behavior is consistent and secure.

---

## 🧠 Lessons Learned

- Business logic vulnerabilities are not caused only by input errors; they are often caused by workflow design flaws.
- Server-side validation is critical.
- Atomic operations, such as DynamoDB conditional writes, are essential in concurrent systems.
- Never trust request timing; enforce state transitions strictly.
