# Security Operations Automation

An automated SecOps orchestration pipeline implemented as an **Azure Function App (Python v2 programming model)**. This tool runs on a regular 15-minute schedule to ingest high-verdict threat investigations from the SecOps Case API, classify them based on confidence scores, route them to respective high-priority or review webhooks, and push automated true-positive feedback back to SecOps Analyst.

## 🛠️ Pipeline Architecture & Logic

Every 15 minutes, the automated timer function executes the following workflow sequentially:

┌─────────────────────────────────┐
│   SecOps TAM Investigations API │
└────────────────┬────────────────┘
│  Fetch (verdict == 'Threat')
▼
┌───────────────────────────┐
│  Confidence Score Filter  │
└──────┬─────────────┬──────┘
│             │
Score >= 0.8         Score < 0.8
│             │
▼             ▼
┌──────────────────────┐┌──────────────────────┐
│  High-Priority Queue ││     Review Queue     │
│   (Webhook Push)     ││    (Webhook Push)    │
└──────────┬───────────┘└──────────────────────┘
│
▼
┌──────────────────────┐
│ Post True Positive   │
│ Feedback to SecOps   │
└──────────────────────┘

1. **Ingest**: Fetches real-time alert data from SecOps matching `verdict: "Threat"`.
2. **Triage & Queue**:
   * **High Priority ($\ge 0.8$ confidence)**: Routed to the high-priority incident queue.
   * **Review Queue ($< 0.8$ confidence)**: Routed to the lower-priority analyst triage queue.
3. **Feedback Loop**: Automatically posts a `true_positive` resolution state back to the SecOps Feedback API for all processed high-confidence threats to tune upstream models.

---

## 📂 Repository Structure

```text
.
├── ARM/
│   └── azuredeploy.json       # Infrastructure-as-Code ARM template
├── function_app.py            # Primary Azure Function application entry point
├── host.json                  # Global configurations for Azure Function workers
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
🚀

Local Development & Setup
Prerequisites
Python 3.10 or 3.11

Azure Functions Core Tools v4 (for local testing and deployments)

An active Azure Subscription

1. Environment Setup
Clone the repository and spin up a virtual environment:

Bash
# Clone the repository
git clone <your-repo-url>
cd <repo-name>

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

2. Local Configuration
Create a local.settings.json file in the root directory to run and test the functions locally without deploying to Azure:

JSON
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}


3. Run Locally
Start the function runtime locally. The timer is configured to run every 15 minutes, but the Core Tools console will allow you to manually trigger it for testing:

Bash
func start

☁️ Production Deployment to Azure
Deploying this application requires creating the cloud infrastructure using the provided ARM template and pushing the application code.

Step 1: Infrastructure Provisioning (ARM)
Use the Azure CLI to deploy the ARM template found in the repository. This provisions a Linux Consumption Plan, a Storage Account, Log Analytics, and Application Insights.

Bash
az deployment group create \
  --resource-group <Your-Resource-Group-Name> \
  --template-file ./ARM/azuredeploy.json \
  --parameters appName=<Your-Unique-Function-App-Name>
Step 2: Code Deployment
Once the infrastructure is ready, use the Azure Functions Core Tools to package and publish the code to your newly created Azure Function App:

Bash
func azure functionapp publish <Your-Unique-Function-App-Name>
📈 Monitoring & Observability
Telemetry data, function runtime logs, and network performance indicators (HTTP connection failures or API latency issues) are streamed automatically to Azure Application Insights.

To view active execution trends, errors, or custom logging.info() statements outputs:

Navigate to the Azure Portal.

Select your deployed Function App.

Under the Monitoring section on the left panel, click on Log Stream (for real-time streaming logs) or Application Insights (for deep diagnostics and query tracing).


---

### Tips for this layout:
* Place the ARM template json inside an `ARM/` folder relative to where you save this `README.md`, or modify the pathing in the deployment commands to reflect where you save your infrastructure file. 
* It uses standard Markdown tables and ASCII diagrams to keep your deployment workflows visual and human-readable.
