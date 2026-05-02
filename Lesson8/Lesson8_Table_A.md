# Lesson 8 — Table A: Structured Operation and Security Analysis

| Vulnerability | Intended Rule(s) | Artifacts Used | Normal Behavior | Exploit Behavior |
|---|---|---|---|---|
| Lesson 8 — Logic Vulnerability / Race Condition | A paid order must not be modified. Billing and update operations must follow strict workflow sequencing. | Browser flow, API requests, Lambda code, DynamoDB order status, CloudShell output, screenshots. | User creates an order, adds shipping, pays, and the order becomes paid/processed. | Billing and update requests are sent concurrently. Before the fix, billing could complete while an update still succeeded, causing a paid order to be modified. |
