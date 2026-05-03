# Lesson 2 — Broken Authentication

## 🎯 Summary
The application incorrectly trusts JWT payload data without verifying its signature, allowing user impersonation.

---

## 🔓 Exploit

### Steps
1. Capture JWT token from DevTools
2. Decode payload
3. Modify:
    - username
    - sub
4. Re-encode token
5. Send API request

---

## 🚨 Result
- Normal → User1 sees own orders
- Exploit → User1 sees User2 orders

---

## 📸 Evidence
See screenshots:
- normal_user1.png
- exploit_user2.png

---

## 🛠️ Fix

### Root Cause
JWT signature not verified

### Fix
- Verify JWT using Cognito JWKS
- Validate:
    - signature
    - issuer
    - expiration

---

## ✅ Verification
- Fake token → rejected
- Real token → works

---

## 🔐 lesson learned
JWT must be verified cryptographically, not just decoded.