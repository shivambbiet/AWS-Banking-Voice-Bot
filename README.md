# AWS Banking Voice Bot

Serverless banking chatbot built with Amazon Connect, Lex, Lambda, and DynamoDB to automate customer support — OTP verification, account validation, repayment flow handling, and query management.

## Architecture

Customer Call → Amazon Connect → Amazon Lex (NLU) → AWS Lambda → DynamoDB
                                                          ↓
                                                    Amazon SNS (OTP delivery)

## Features
- OTP-based customer verification via SNS
- Account validation and balance lookup
- Conversational call flows for banking support
- Serverless, event-driven architecture

## Tech Stack
- **Amazon Connect** – call flow / IVR
- **Amazon Lex** – intent recognition & NLU
- **AWS Lambda** – business logic (Python)
- **DynamoDB** – customer & account data
- **Amazon SNS** – OTP delivery via SMS

## Project Structure
\`\`\`
lambda/
  ├── otp_verification.py
  └── account_validation.py
lex-bot-export/
  └── bot_config.json
requirements.txt
\`\`\`

## Setup
1. Create DynamoDB tables: `CustomerOTPTable`, `CustomerAccountsTable`
2. Deploy Lambda functions from `/lambda`
3. Import Lex bot from `/lex-bot-export`
4. Connect Lex bot to Amazon Connect contact flow
5. Configure SNS for OTP delivery

## Author
Shivam
