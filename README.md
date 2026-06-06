🛠 Cloud Infrastructure Stack
The included Azure Resource Manager (azuredeploy.json) template automates the provisioning of an enterprise-ready serverless environment:

Azure Function App (Linux, Python): Hosts and executes your serverless security logic.

App Service Plan (Consumption Plan / Y1 Tier): Serverless compute allocation that automatically scales to zero when idle, removing fixed monthly overhead.

Azure Storage Account (LRS): Required by the function runtime engine for internal state management, coordination keys, and locks.

Application Insights: Provides live log streams, performance tracking, and transaction maps to trace API connections.

🚀 Deployment Workflow
1. Provision Infrastructure via Azure CLI
Authenticate to your active tenant, establish a dedicated resource group, and spin up the backend architecture:

Bash
# Authenticate to Azure
az login

# Create a resource group in your preferred location
az group create --name ARM-SecOps-RG --location eastus

# Run the deployment template
az deployment group create \\
  --resource-group ARM-SecOps-RG \\
  --template-file azuredeploy.json \\
  --parameters appName=secops-orchestrator
