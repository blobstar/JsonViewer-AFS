import os
import json
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

STORAGE_MODE = os.getenv('STORAGE_MODE', 'local')

print(f"STORAGE_MODE: {STORAGE_MODE}")

if STORAGE_MODE == 'azure':
    print("\nTesting Azure Storage Connection...")
    try:
        AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        AZURE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME', 'afs')
        
        print(f"Connection String: {AZURE_STORAGE_CONNECTION_STRING[:50]}...")
        print(f"Container Name: {AZURE_CONTAINER_NAME}")
        
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
        # List blobs
        blobs = container_client.list_blobs()
        files = [blob.name for blob in blobs if blob.name.endswith('.json')]
        
        print(f"\n✓ Successfully connected to Azure!")
        print(f"Found {len(files)} JSON files in container '{AZURE_CONTAINER_NAME}':")
        for f in files[:10]:
            print(f"  - {f}")
            
    except Exception as e:
        print(f"\n✗ Error connecting to Azure: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("\nTesting Local Storage Connection...")
    LOCAL_JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_output'))
    print(f"LOCAL_JSON_DIR: {LOCAL_JSON_DIR}")
    print(f"Directory exists: {os.path.exists(LOCAL_JSON_DIR)}")

    if os.path.exists(LOCAL_JSON_DIR):
        files = [f for f in os.listdir(LOCAL_JSON_DIR) if f.endswith('.json')]
        print(f"✓ Found {len(files)} JSON files:")
        for f in files[:5]:
            print(f"  - {f}")
    else:
        print("✗ Directory not found!")
