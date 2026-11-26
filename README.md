# streamguard-bedrock-agent
AI Refund Agent with layered security boundaries built on Amazon Bedrock AgentCore
# StreamGuard: Bounded AI Refund Agent on Amazon Bedrock AgentCore

**StreamGuard** is an automated subscription refund agent built on the **Amazon Bedrock AgentCore managed harness** using **Amazon Nova Lite**. It enforces strict financial, behavioral, and security boundaries through layered cloud controls rather than relying solely on system prompts.

## Architecture
`User` -> `Amazon Bedrock AgentCore (StreamGuardAgent)` -> `AgentCore Gateway` -> `AWS Lambda (Business Logic)` -> `Amazon DynamoDB (Least-Privilege IAM)`

## Hard Boundaries Enforced
1. **Financial Cap:** Automated refunds are strictly capped at **$50.00**. Higher amounts return `ESCALATE_TO_HUMAN`.
2. **Consumption Limit:** Denies refunds if the user watched more than **10%** of the content.
3. **Fraud Prevention:** Automatically blocks accounts flagged with `CHARGEBACK_HISTORY`.
4. **Idempotency:** Prevents duplicate refunds on already `REFUNDED` subscriptions.
5. **Data Isolation:** IAM policy explicitly denies `dynamodb:Scan` and `dynamodb:DeleteItem`.

## Repository Contents
- `lambda_function.py`: Core deterministic validation logic executed via AWS Lambda.
- `tool_schema.json`: MCP tool definition used in the Amazon Bedrock AgentCore Gateway.
- `iam_least_privilege_policy.json`: Scoped IAM policy restricting database access.
