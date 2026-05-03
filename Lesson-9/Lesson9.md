# Lesson 9 : Vulnerable Dependencies
## Vulnerability overview
The vulnerable implementation uses node-serialize to deserialize untrusted input from API Gateway requests:
- serialize.unserialize(event.body)
- serialize.unserialize(event.headers)
This allows attacker-controlled input to be converted into executable JavaScript objects. Since the library supports function reconstruction, it can lead to Remote Code Execution (RCE) if malicious payloads are provided.
The issue is worsened by the fact that Lambda processes external API requests, making the deserialization step a direct attack entry point.
## Impact
If exploited, this vulnerability can allow an attacker to:
- Execute arbitrary JavaScript code inside the Lambda environment
- Manipulate backend logic and trigger internal Lambda functions
## Fix Implementation
1. Add a checker that checks if _$$ND_FUNC$$_ is exist in the input
2. If it exists it will return "malicious input blocked" ant terminate.
   
