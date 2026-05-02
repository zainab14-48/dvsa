# Lesson 8 — Table B: Deviation and Fix Summary

| Vulnerability | Why This Is a Deviation | Deviation Class | Fix Applied | Post-Fix Verification |
|---|---|---|---|---|
| Lesson 8 — Logic Vulnerability / Race Condition | The exploit violates the intended order workflow because a paid order should be locked from user-controlled cart or shipping changes. Allowing updates after billing can create inconsistent payment and order data. | Intentional misuse / logic flaw / race condition | Added server-side status validation and DynamoDB `ConditionExpression="orderStatus < :paid"` in the order update workflow. | Re-running the race condition shows billing succeeds once, while the update is rejected with `order already paid`. |
