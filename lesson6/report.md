# Lesson 6: Denial of Service (DoS)

## Part 1) Goal and Vulnerability Summary
This lesson demonstrates a Denial of Service (DoS) weakness in the billing path of the DVSA serverless application. The main affected components are the public API entry point and the billing-related backend processing functions. The security impact is that repeated concurrent requests can exhaust limited processing capacity, which may delay, throttle, or prevent legitimate users from completing payment. At a high level, the weakness is insufficient abuse protection and lack of fair request handling for a sensitive backend workflow.

## Part 2) Why This Works / Root Cause
The vulnerability is possible because the billing path accepts repeated requests without strong rate limiting or abuse controls. Since serverless backends still have bounded concurrency and practical processing limits, repeated parallel requests can saturate the path and reduce availability for legitimate users. The weakness is therefore in request-handling design and resource protection, not in confidentiality.

## Part 3) Environment and Setup
The DVSA environment was deployed in AWS `us-east-1`. The application was accessed through the DVSA website URL and the billing-related backend path was studied through the AWS Console and related API/Lambda resources. Relevant services included API Gateway, billing-related Lambda functions, Cognito authentication, and CloudWatch logs for observing request handling and backend behavior.

Tools used:
- AWS Console
- browser
- terminal
- CloudWatch logs

Relevant components examined:
- billing-related API path
- billing Lambda or related order/payment Lambda functions
- CloudWatch logs for request behavior
- configuration before and after fix

## Part 4) Reproduction Steps
1. Open the DVSA environment and verify that the application is working normally.
2. Identify the billing-related API path or backend processing function.
3. Observe the expected normal behavior for a legitimate billing request.
4. Send repeated parallel requests to the billing path in the controlled lab environment.
5. Monitor the responses and observe any slowdown, failure, throttling, or service degradation.
6. Open CloudWatch logs and inspect backend behavior during the request burst.
7. Record the evidence showing reduced availability or abnormal handling under load.

## Part 5) Evidence and Proof
The proof for this lesson includes:
- terminal output showing repeated billing requests
- response failures, throttling, or degraded behavior
- CloudWatch logs from the relevant Lambda function(s)
- screenshots of configuration before mitigation
- post-fix comparison showing improved resilience

The key proof is that the billing path does not handle repeated concurrent requests fairly and may impact legitimate users.

## Part 6) Fix Strategy / Probable Mitigation
The weakness should be mitigated by protecting the billing path against abuse. Appropriate controls include:
- rate limiting at the API layer
- throttling controls for the relevant API route
- fair request controls such as per-user/per-client limits
- isolating sensitive backend concurrency
- where useful, queue-based request handling or better workflow protection

These mitigations address the root cause by preventing a single abusive pattern from consuming disproportionate backend processing capacity.

## Part 7) Code / Config Changes
The fix was applied in the backend/API protection layer for the billing workflow. The exact mitigation may include one or more of the following:
- reduced or controlled request rate for the billing route
- throttling configuration at API Gateway
- reserved concurrency or tighter request-handling protection for the billing Lambda
- workflow changes to reduce direct abuse of sensitive billing operations

Example summary:
- before fix: billing path accepted repeated concurrent requests with insufficient protection
- after fix: request limits and backend protection were added to reduce saturation risk

Changed resources / areas:
- billing-related API configuration
- billing-related Lambda protection settings
- any relevant server-side workflow guards

## Part 8) Verification After Fix
After the fix was applied, the same repeated request pattern no longer caused the same level of service degradation. The billing path became more resistant to abuse, and legitimate behavior remained available. Post-fix screenshots and logs showed safer handling of repeated requests and improved backend stability.

## Part 9) Structured Operation and Security Analysis

### 1) Intended Logic and Security Rule(s)
Under normal conditions, a user submits a billing request through the frontend. The request is sent to API Gateway, which invokes the relevant billing backend logic in Lambda. The billing function processes one valid billing operation for the authenticated user and updates the necessary backend state. The correct outcome is that legitimate payment requests are handled promptly and fairly.

Security rules:
- billing capacity must not be easily consumed by abusive repeated requests
- legitimate users must retain fair access to the billing workflow
- public-facing request paths must include abuse protection for sensitive operations

### 2) Evidence Sources and Behavior Trace
Artifacts used:
- browser workflow
- terminal request output
- API responses
- CloudWatch logs
- AWS configuration screenshots
- before/after fix comparison

Behavior comparison:
- normal: single legitimate billing request is handled normally
- exploit/abuse: repeated concurrent billing requests reduce availability or trigger failures
- post-fix: abusive request pattern is limited, and normal requests remain more stable

### 3) Deviation Analysis and Classification
The exploit behavior deviates from the intended rule because the billing path should remain reasonably available to legitimate users and should not be easily exhausted by abusive repeated requests. The evidence shows that request handling before the fix did not provide fair protection against repeated parallel use.

Deviation class:
- Intentional misuse / security-relevant abuse

### 4) Explainable Fix and Post-Fix Validation
The incorrect assumption was that the billing path could safely accept repeated requests without stronger abuse control. The fix belongs in the API/backend protection layer. The applied changes added throttling, rate limiting, or request-handling protections to reduce the risk of saturation. Post-fix verification showed that the same abuse pattern no longer produced the same unsafe availability impact, while legitimate behavior still worked.

## Part 10) Takeaway / Lessons Learned
This lesson shows that serverless systems are still vulnerable to availability abuse when sensitive routes are not protected against repeated parallel requests. Even though the platform scales automatically, critical paths still need explicit fairness and abuse controls. The key secure design lesson is to apply rate limiting, workflow protection, and resource isolation to sensitive operations such as billing.
