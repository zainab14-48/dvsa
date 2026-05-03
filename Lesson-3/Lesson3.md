# Lesson 9 : Vulnerable Dependencies
## Vulnerability overview
in backend receipt-handling functionality. Privileged operations can be abused to generate access to receipt files stored in Amazon S3, including pre-signed download links. If authorization is not properly enforced, unauthorized users may obtain these links and access restricted data.

The root cause is insufficient role-based access control around receipt generation and file exposure. To fix this issue, strict authorization must be enforced on all receipt-related endpoints, access to signed URLs must be limited to authorized roles only, and direct exposure of S3 objects should be minimized.
## Impact
If exploited, this vulnerability can allow an attacker to:
- Unauthorized access to sensitive receipt files stored in Amazon S3
- Exposure of confidential user and transaction information
- Loss of trust and possible compliance/security policy violations
## Fix Implementation
1. Implemented secure authentication check by retrieving user claims from API Gateway authorizer context
2. Added error handling to prevent unauthorized access when authentication data is missing.
3. Enforced role-based access control (RBAC) using Cognito groups to distinguish between admin and normal users.
4. Restricted receipt access using user-specific S3 prefixes, preventing cross-user data exposure