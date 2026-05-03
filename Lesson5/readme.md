# DVSA Lesson 5 – Broken Access Control (ICS344)

This repository documents a Broken Access Control vulnerability in the Damn Vulnerable Serverless Application (DVSA) and the fixes applied.

> “This lesson demonstrates a Broken Access Control vulnerability affecting the DVSA backend. The main impacted components are the DVSA-ORDER-MANAGER Lambda (due to unsafe deserialization) and the DVSA-ADMIN-UPDATE-ORDERS Lambda (due to missing authorization checks).”


## Vulnerability summary

The vulnerability is caused by:

- **Unsafe deserialization** in `DVSA-ORDER-MANAGER` using `node-serialize`, allowing attacker-controlled JavaScript execution inside the Lambda.
- **Missing role-based authorization** in `DVSA-ADMIN-UPDATE-ORDERS`, allowing any caller to perform admin-level order updates once invoked.

This leads to **privilege escalation** where a normal user can update order status (e.g., mark an order as `paid`) without admin privileges or payment verification.

## Affected components

- **Lambda**
  - `DVSA-ORDER-MANAGER` (public, vulnerable to code injection, over-privileged IAM role)
  - `DVSA-ADMIN-UPDATE-ORDERS` (internal admin function, updates DynamoDB)
- **DynamoDB**
  - `DVSA-ORDERS-DB` table (stores order records, status, total, confirmation token)
- **API Gateway**
  - Public `/order` endpoint on

## Exploit overview

1. **Log in** to the DVSA web app and create an order.
2. **Capture the JWT** from the `Authorization` header using Chrome DevTools.
3. **Decode the JWT** on `jwt.io` and extract:
   - `sub` / `username` → user ID
4. **Send a malicious payload** to the public `/order` endpoint that:
   - Exploits `node-serialize` to execute injected JavaScript.
   - Uses the AWS Lambda SDK to invoke `DVSA-ADMIN-UPDATE-ORDERS` with a crafted event body.
5. **Result:** Order status in `DVSA-ORDERS-DB` is updated to `paid` for a normal user.

Example effect (from the lab):

- Order `ced784b1-51b6-476f-abb1-0d8a5c0062d1` changed to status `paid` with confirmation `FREE_RIDE_TOKEN` and total `$0`.

## Fix strategy

### Remove unsafe deserialization in `DVSA-ORDER-MANAGER`
