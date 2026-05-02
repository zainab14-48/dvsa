# ICS344 – Lesson 7  
---

# Part 1 – Goal & Vulnerability Summary
The DVSA Lambda function `DVSA-SEND-RECEIPT-EMAIL` is assigned an IAM role with excessive permissions such as `s3:*`, `dynamodb:*`, and `ses:*`.  
This violates the principle of least privilege and allows attackers to misuse temporary credentials leaked in CloudWatch logs.

---

# Part 2 – Root Cause
The Lambda execution role includes broad wildcard permissions instead of minimal SES + CloudWatch Logs permissions.

---

# Part 3 – Environment & Setup
- Lambda: DVSA-SEND-RECEIPT-EMAIL  
- IAM Execution Role  
- CloudWatch Logs  
- S3 Trigger Bucket  
- AWS CLI on Ubuntu (WSL)  

---

# Part 4 – Reproduction Steps
1. Upload a file to DVSA website to trigger Lambda.  
2. Open CloudWatch logs → extract temporary credentials.  
3. Use AWS CLI to perform unauthorized DynamoDB actions.  
4. The scan succeeds → proving excessive permissions.

---

# Part 5 – Evidence
Screenshots included in `/evidence` folder:
- CloudWatch logs showing AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN  
- IAM role with wildcard permissions  
- Successful DynamoDB scan  
- S3 trigger evidence  

---

# Part 6 – Fix Strategy
Apply least-privilege IAM:
- Remove wildcard permissions  
- Allow only:
  - `ses:SendEmail`
  - CloudWatch Logs permissions  
- Restrict S3 access to the specific bucket  
- Restrict DynamoDB access to only required tables  

---

# Part 7 – Code / Config Changes
Included in `/code` folder:
- vulnerable-iam-policy.json  
- fixed-iam-policy.json  

---

# Part 8 – Verification
After applying the fix:
- DynamoDB scan is denied  
- Only SES SendEmail is allowed  
- Lambda still works normally  
