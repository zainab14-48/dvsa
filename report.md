# Lesson 1: Event Injection

## Part 1: Goal and Vulnerability Summary
The goal of this lesson is to demonstrate an Event Injection vulnerability in a serverless application.  
The issue occurs when attacker-controlled input is processed in an unsafe manner, allowing unintended backend behavior.  
The vulnerability affects the API Gateway → Lambda processing logic.

---

## Part 2: Root Cause
The root cause is unsafe handling of user-controlled input.  
The backend assumes input is safe and does not enforce strict validation.  
This allows malicious or unexpected structures to reach the application logic.

---

## Part 3: Environment and Setup
- Region: us-east-1
- CloudFormation Stack: serverlessrepo-OWASP-DVSA
- Website:
http://dvsa-zainab-2026-xyz-883425316372-us-east-1.s3-website.us-east-1.amazonaws.com
- API Endpoint:
https://49zzme9ri9.execute-api.us-east-1.amazonaws.com/dvsa
- Services used:
  - API Gateway
  - AWS Lambda
  - Amazon Cognito
  - CloudWatch
- Tools:
  - Browser
  - AWS Console
  - Terminal

---

## Part 4: Reproduction Steps
1. Open DVSA website
2. Login successfully
3. Identify API endpoint
4. Send request to backend
5. Observe response
6. Check CloudWatch logs

---

## Part 5: Evidence and Proof
Evidence includes:
- API responses
- CloudWatch logs
- AWS Console screenshots
- Website behavior

---

## Part 6: Fix Strategy
- Validate all incoming requests
- Reject unexpected input fields
- Treat all input as data only
- Remove unsafe processing logic

---

## Part 7: Code / Config Changes
Example fix:
- Added validation layer before processing request
- Ensured only allowed fields are accepted

---

## Part 8: Verification After Fix
- Re-tested API
- Invalid input no longer accepted
- Application behaves normally

---

## Part 9: Structured Analysis

### Intended Logic
User → API Gateway → Lambda → Backend → Response

### Security Rule
User input must never be executed or trusted.

### Deviation
Application processes untrusted input without validation.

### Fix Validation
After fix, input is validated and no unsafe behavior occurs.

---

## Part 10: Takeaway
Event Injection vulnerabilities occur when input is not validated.  
Proper validation and secure coding practices prevent such issues.