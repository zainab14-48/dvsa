# DVSA Lesson 1 – Event Injection

## Overview
This repository documents the implementation, analysis, and mitigation of an Event Injection vulnerability in a serverless AWS application (OWASP DVSA).

## Environment
- AWS Region: us-east-1
- Services: API Gateway, Lambda, Cognito, CloudWatch
- Application: OWASP DVSA

## Vulnerability
The vulnerability exists in the Lambda function `DVSA-ORDER-MANAGER`, where unsafe deserialization of user input allows execution of malicious payloads.

## Fix Summary
- Removed node-serialize usage
- Replaced with JSON.parse
- Added strict input validation
- Prevented unsafe input execution

## Verification
After applying the fix:
- Malicious input is rejected
- No unsafe behavior occurs
- Normal functionality remains intact

## Structure
- lesson1/report.md → Full report
- lesson1/evidence → Screenshots
- lesson1/tables → Analysis tables
 
