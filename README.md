## Introduction
Tenalyse is an AI-powered tenancy contract analyzer designed to simplify and streamline the process of reviewing rental agreements. 

Tenancy contracts are often riddled with complex legal language, vague clauses, and hidden obligations that most tenants struggle to fully understand. As a result, people are frequently blindsided by terms they didn’t realize they agreed to, leading to financial loss, legal disputes, and immense stress.
According to Shelter UK, A UK survey found that 1 in 4 renters faced surprise charges or conditions due to unnoticed clauses in their tenancy agreements. Thereby, displaying a pressing need for a transparent, intelligent tool that helps tenants and landlords clearly understand what's in their contracts, before it's too late[^1].

Built using AWS Lambda as its backbone, Tenalyse intelligently scans tenancy contracts, identifies key clauses, flags potential issues, and highlights crucial details, thereby making legal documents more transparent and accessible for everyone.

Tenalyse ensures tenants are never caught off-guard by legal jargon again.

## How to use
1. Upload a tenancy contract to our website: **https://d36zj33ar35qel.cloudfront.net**.  You can use one of the sample contracts from the "Tenancy Agreement" folder or upload your own.
2. Wait for the results. Processing time depends on the size of the file, but it typically completes within a few seconds for most documents.

## How Tenalyser Works

### 1. Upload Through a Seamless Web Interface  
Users start at our lightweight web portal:  
**https://d36zj33ar35qel.cloudfront.net**  
This static front-end is globally distributed for low-latency, fast interaction, and zero cold starts.

### 2. Secure, Efficient File Uploads via Presigned URLs 
The front-end uploads the files to our s3 bucket through a presigned url. It then uses this url to upload the contract directly to our S3 bucket.

**Why this matters:**  
This keeps our backend stateless and secure, reducing risk and preventing unauthorised access while improving performance. By offloading file transfer to S3, our system avoids bottlenecks, improves upload reliability, and saves compute time.

### 3. Event-Driven Architecture Triggers PDF Processing  
Once a contract lands in S3, it **automatically triggers** our backend contract-processing pipeline—no polling, no latency. This makes the service fully event-driven.

**Why this matters:**  
This ensures scalability and responsiveness, especially under load. Files are processed immediately without any manual intervention or scheduling logic.

### 4. Asynchronous PDF Text Extraction  
A Lambda function is triggered to read and extract the contract text. It handles:
- Converting the PDF to raw text
- Splitting large documents into smaller chunks to be within model limits
- Logging and tracking progress

**Why this matters:**  
Text extraction is handled off the main thread using `asyncio` and multithreading. This minimizes time per batch and lets multiple documents be processed in parallel, improving throughput.

### 5. Language Model Analysis Tailored to Tenancy Contracts  
Each text chunk is passed to an LLM (OpenAI or Bedrock). The prompt is carefully engineered to:
- Extract relevant legal clauses (rent, duration, notice period, etc.)
- Summarize them in plain English
- Flag unclear or risky language
- Offer negotiation suggestions
Results are appended batch-by-batch to ensure even partial analysis is recoverable to ensure resiliency
**Why this matters:**  
We're not using generic AI outputs, we're extracting actionable, contract-specific insights with user safety and clarity in mind. Each result is useful even to users with no legal background.

### 6. Smart State Management and Storage in DynamoDB  
Each result, along with a unique file ID, current status, summary and last update time, is stored in DynamoDB. 
**Why this matters:**  
By writing once after the analysis completes, we reduce the number of write operations, saving cost and complexity. This also ensures that users only receive complete, validated summaries—eliminating the need to handle partial or inconsistent states in the UI. DynamoDB’s low-latency and high-availability guarantees make it ideal for real-time retrieval of contract summaries.

### 7. Users Access Results Instantly  
The frontend polls our backend via an API to check on analysis progress and fetch results once they’re ready.

**Why this matters:**  
Polling ensures the frontend stays responsive without requiring websockets or long-lived connections. It's simple and robust across unreliable mobile and WiFi connections.

---

## 🧪 Tech Stack (Chosen to Fit the Problem, Not Just the Tools)

| Component         | Role in System                                                                 |
|------------------|---------------------------------------------------------------------------------|
| CloudFront        | Frontend delivery; fast, serverless, always up                                 |
| S3                | File storage and event triggering; decouples file ingestion and processing     |
| Lambda            | Async PDF text extraction, chunking, and AI orchestration                      |
| API Gateway       | Handles presigned URL generation and result polling                           |
| DynamoDB          | Low-latency storage for results, status, and file tracking                     |
| OpenAI / Bedrock  | Domain-specific LLM analysis                                                    |
| Python & Asyncio  | Efficient backend processing and concurrency management                        |

---

## 🔍 What Makes This Service Stand Out

**Every architectural choice supports our product goal:**  
To give non-legal users fast, clear, trustworthy insights from long and complex tenancy documents.

- **Security-first uploads** prevent unauthorized access and reduce backend exposure.
- **True event-driven logic** ensures the system reacts instantly to user actions.
- **Async processing and chunking** make it scalable and token-limit safe.
- **LLM orchestration and prompt design** deliver genuinely helpful summaries.
- **Resilient state tracking** keeps users informed, even during high load or failure.
- **Serverless design** means zero-maintenance scaling—perfect for high-traffic use or rapid hackathon deployment.

## Why Tenalyse Stands Out
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

[^1]: https://publications.parliament.uk/pa/cm201314/cmselect/cmcomloc/50/50ii05.htm?utm_source=chatgpt.com



