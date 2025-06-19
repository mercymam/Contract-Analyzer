## Introduction
Tenanalyze is an AI-powered tenancy contract analyzer designed to simplify and streamline the process of reviewing rental agreements. 

Tenancy contracts are often riddled with complex legal language, vague clauses, and hidden obligations that most tenants—and even some landlords—struggle to fully understand. As a result, people are frequently blindsided by terms they didn’t realize they agreed to, leading to financial loss, legal disputes, and immense stress.
According to Shelter UK, A UK survey found that 1 in 5 renters faced surprise charges or conditions due to unnoticed clauses in their tenancy agreements. Thereby, displaying a pressing need for a transparent, intelligent tool that helps tenants and landlords clearly understand what's in their contracts—before it's too late.

Built using AWS Lambda as its backbone, Tenanalyze intelligently scans tenancy contracts, identifies key clauses, flags potential issues, and highlights crucial details, thereby making legal documents more transparent and accessible for everyone.

Whether you're a tenant, landlord, or property manager, Tenanalyze ensures you're never caught off-guard by legal jargon again.

## How It Works
Upload Your Contract
Users upload their tenancy agreements via a web interface or API.

Trigger the Analyzer
This upload event triggers an AWS Lambda function via S3 Event Notifications, kicking off the contract analysis pipeline.

AI Contract Processing
Our Lambda function invokes an AI model (powered by OpenAI or AWS Bedrock) that:

Parses the document

Extracts clauses (e.g., rent amount, duration, termination terms)

Classifies them as positive, warning, or critical

Flags vague or unfair terms

Smart Summaries and Insights
The output includes:

A clause-by-clause breakdown

Smart summaries for non-lawyers

Potential red flags

Suggestions for negotiation

View Results
Results are stored in S3, retrievable through a user interface or API endpoint (powered by API Gateway + Lambda).

## Tech Stack
AWS Lambda – Core compute layer for event-driven processing

Amazon S3 – Stores uploaded contracts and analysis reports

API Gateway – Triggers Lambda for on-demand analysis

OpenAI / AWS Bedrock – Natural language processing and clause classification

Python – Backend logic and orchestration

## Real-World Problem Solved
### Legal Complexity
Most tenancy agreements are filled with complex language that overwhelms the average person. Tenanalyze decodes these documents using AI.

### Risk Mitigation
By flagging ambiguous or unfair clauses, tenants and landlords can avoid costly disputes.

### Time Savings
Manual review of rental agreements is time-consuming. Tenanalyze delivers actionable insights in seconds.

### Scalability
Built on AWS Lambda, our solution scales automatically—whether you're analyzing one contract or one million.

## Why Tenanalyze Stands Out
#### Clause Intelligence: Goes beyond keyword search—understands context and intent.

#### AI-First: Leverages the latest in NLP for legal document parsing.

#### Built for Everyone: Designed with accessibility in mind—no legal background required.

## Future Enhancements
#### Real-time chatbot assistant to answer contract-specific questions

#### Support for other contract types (employment, service agreements)

## Made for the AWS Lambda Hackathon Challenge
Challenge Requirement: Build a serverless application using AWS Lambda with at least one trigger to solve a real-world business problem.

✅ Uses AWS Lambda as the core compute layer
✅ S3 event triggers to invoke Lambda functions
✅ Solves a real-world problem in legal tech
✅ Integrates optional services like S3 and AI (OpenAI or AWS Bedrock)

### Built With Passion by Clouders
Because understanding your rights shouldn't require a law degree.

