# Lesson 8 — Tables

## Table A: Structured Operation and Security Analysis

| Vulnerability | Intended Rule(s) | Artifacts Used | Normal Behavior | Exploit Behavior |
|---|---|---|---|---|
| Lesson 8 — Logic Vulnerability / Race Condition | A paid order must not be modified. Billing and update operations must follow strict workflow sequencing. | Browser flow, API requests, Lambda code, DynamoDB order status, CloudShell output, screenshots. | User creates an order, adds shipping, pays, and the order becomes paid/processed. | Billing and update requests are sent concurrently. Before the fix, billing could complete while an update still succeeded, causing a paid order to be modified. |

## Table B: Deviation and Fix Summary

| Vulnerability | Why This Is a Deviation | Deviation Class | Fix Applied | Post-Fix Verification |
|---|---|---|---|---|
| Lesson 8 — Logic Vulnerability / Race Condition | The exploit violates the intended order workflow because a paid order should be locked from user-controlled cart or shipping changes. Allowing updates after billing can create inconsistent payment and order data. | Intentional misuse / logic flaw / race condition | Added server-side status validation and DynamoDB `ConditionExpression="orderStatus < :paid"` in the order update workflow. | Re-running the race condition shows billing succeeds once, while the update is rejected with `order already paid`. |
