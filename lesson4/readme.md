# Lesson 4 — Insecure Cloud Configuration

## 🎯 Summary
The S3 bucket allowed file uploads that were automatically processed by a Lambda function without validation.

---

## 🔓 Exploit

### Steps
1. Upload file to S3 bucket
2. Lambda is triggered automatically
3. File is processed without validation

---

## 🚨 Result
- Lambda executed on attacker-controlled input
- Errors observed in logs

---

## 📸 Evidence
- S3 upload
- Lambda logs showing processing
- Error messages

---

## 🛠️ Fix

### Root Cause
- Overly permissive S3 access
- No input validation in Lambda

---

### Fix Applied
1. Restricted S3 bucket access
2. Added validation in Lambda:
    - file name
    - file type

---

## ✅ Verification
- Invalid files rejected
- Lambda stops execution

---

## 🔐 lesson learned
Cloud misconfiguration + lack of validation leads to dangerous backend processing.

