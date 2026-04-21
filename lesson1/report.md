# Lesson 1: Event Injection

## Part 1: Goal and Vulnerability Summary
This lesson demonstrates an Event Injection vulnerability in a serverless application.  
The issue occurs when user input is processed in an unsafe way, allowing unintended behavior.

---

## Part 2: Root Cause
The vulnerability is caused by unsafe deserialization using:

var req = serialize.unserialize(event.body);

This allows execution of malicious input.

---

## Part 3: Environment and Setup
- Region: us-east-1
- Stack: serverlessrepo-OWASP-DVSA
- Website: http://dvsa-zainab-2026-xyz-883425316372-us-east-1.s3-website.us-east-1.amazonaws.com
- API: https://49zzme9ri9.execute-api.us-east-1.amazonaws.com/dvsa

---

## Part 4: Reproduction Steps
1. Open DVSA website
2. Login
3. Send request to API
4. Observe response
5. Check logs

---

## Part 5: Evidence
- API responses
- CloudWatch logs
- Lambda code

---

## Part 6: Fix Strategy
- Remove node-serialize
- Use JSON.parse
- Add validation

---

## Part 7: Code Changes

### Before
var req = serialize.unserialize(event.body);

### After
let req = JSON.parse(event.body);

---

## Part 8: Verification
- Invalid input rejected
- Application works normally

---

## Part 9: Analysis

### Intended Flow
User → API → Lambda → Response

### Rule
Input must not be executed

### Deviation
Input executed as code

---

## Part 10: Takeaway
Always validate input and avoid unsafe deserialization.
