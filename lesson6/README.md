# Lesson 6 – Denial of Service (DoS)

## Overview
This folder documents Lesson 6 of the DVSA project, which focuses on Denial of Service (DoS) in the billing workflow of the serverless application.

## Official Lesson Goal
The objective of this lesson is to show that repeated concurrent billing requests can consume limited processing capacity and prevent legitimate users from completing payment normally. The appropriate fix should involve controls such as rate limiting, abuse protection at the API layer, concurrency isolation, or fair request controls.

## Environment
- AWS Region: us-east-1
- Application: OWASP DVSA
- Services involved:
  - Amazon API Gateway
  - AWS Lambda
  - Amazon Cognito
  - Amazon CloudWatch
  - Billing and order-related backend functions
 
 

## Deliverable Notes
This lesson is organized to match the project submission requirements:
- full report structure
- evidence and proof
- code/config changes
- post-fix verification
- structured analysis tables
