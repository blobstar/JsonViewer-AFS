# JSON Browser

A modern Flask + Tailwind static web app to browse and view JSON files. Supports both local storage and Azure Blob Storage. Only the `fields` objects under the `contents` array in each JSON are shown.

## Features
- Modern dark UI (Tailwind CSS)
- Left navbar with file search
- View all `fields` objects per file
- **Azure Blob Storage support** - Connect to your Azure storage account
- **Local mode** - Use local `test_output` folder
- Ready for Azure deployment

## Setup

### 1. Install dependencies:
```sh
pip install -r requirements.txt
```

### 2. Configure Storage (Choose One)

#### Option A: Local Storage (Development)
Create a `.env` file:
```
STORAGE_MODE=local
```

#### Option B: Azure Blob Storage
Create a `.env` file with your Azure Storage details:
```
STORAGE_MODE=azure
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=YOUR_ACCOUNT;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net
AZURE_STORAGE_CONTAINER_NAME=test-output
```

You can find your connection string in Azure Portal:
- Storage Account → Access Keys → Connection String

### 3. Run the app:
```sh
python app.py
```

Open [http://localhost:5000](http://localhost:5000)

## Azure Deployment

### Prerequisites
- Azure App Service (Python runtime)
- Azure Storage account with JSON files uploaded

### Steps
1. Set environment variables in App Service:
   - `STORAGE_MODE` = `azure`
   - `AZURE_STORAGE_CONNECTION_STRING` = your connection string
   - `AZURE_STORAGE_CONTAINER_NAME` = your container name

2. Deploy using Azure CLI or GitHub Actions:
```sh
az webapp deployment source config-zip --resource-group CaseWare_Mapper --name your-app-name --src app.zip
```

---

**Note:**
- For local mode, ensure `test_output` folder exists at the same level as `json_browser`
- Only `.json` files are listed
- Supports both local directories and Azure Blob Storage containers
