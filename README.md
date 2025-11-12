Stateful Visit Counter Application
🚀 Project Overview: Solving the Serverless Memory Problem
This project is a fully functional, stateful serverless application deployed on AWS. It serves as a proof-of-concept demonstrating how to solve the core challenge of serverless computing: maintaining data between user visits.

The application functions as a Visit Counter that correctly retrieves a user's session from the database, increments the count, and saves the new state before responding.

Video Walkthrough (Recommended for Recruiters): Watch the Full Debugging Story on YouTube https://youtu.be/v0oDWnETL78

Final API URL Proof: [Paste Your Live API URL Here] (e.g., Refreshing this URL proves state is maintained.)

## 🛠️ Technology Stack
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| Serverless Function | AWS Lambda (Python 3.11) | The compute layer that runs the application logic. |
| Infrastructure | AWS SAM (Serverless Application Model) | Defines and deploys all resources via a single template.yaml file. |
| Database/State | AWS DynamoDB (SimpleTable) | Provides persistent, external memory to store the visit_count for each user session. |
| Security | IAM Roles | Securely grants the Lambda function only the DynamoDBCrudPolicy permission needed to read/write to the table. |
| Development | Git & GitHub | Used for version control, collaborative development, and deployment history. |

💡 Key Feature: Achieving Statefulness
This project highlights the ability to build memory into a stateless environment:

Read State: The Lambda function uses the boto3 SDK to table.get_item from DynamoDB using a unique session_id.

Modify State: It converts the count (using Python's int() to handle the DynamoDB Decimal type) and increments it by one.

Write State: It uses table.put_item to save the new visit_count back to the database.


⚙️ Debugging Log (Real-World Skills)
This project documented three critical real-world errors that were diagnosed and fixed:

1. The Decimal Runtime Bug
Problem: The API returned a generic 500 Internal Server Error.

Debug Process: The true error was found by checking the AWS CloudWatch Logs.

Root Cause: The logs showed Object of type Decimal is not JSON serializable.

Solution: The bug was fixed by adding the line visit_count = int(visit_count) to the app.py handler.

2. The Environment PermissionError
Problem: The sam build command failed with a persistent PermissionError.

Root Cause: This was a race condition where the OneDrive file-syncing service was "locking" the temporary .aws-sam folder.

Solution: The reliable fix was to manually delete the temporary .aws-sam folder before running sam build again.

🚀 Deployment & Local Setup
To replicate and test this project, you need the AWS SAM CLI and a Python environment.

Clone the repository: Run git clone https://github.com/Theo7Labs/stateful-lambda-app.git and then cd stateful-lambda-app.

Build: Run sam build (This packages the code and downloads dependencies like boto3).

Deploy: Run sam deploy (This creates the Lambda function, API Gateway, and DynamoDB table).
