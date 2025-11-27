from flask import Flask, render_template, jsonify, send_from_directory, request
import os
import json
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import io

load_dotenv()

app = Flask(__name__)

# Configuration
STORAGE_MODE = os.getenv('STORAGE_MODE', 'local')  # 'local' or 'azure'
LOCAL_JSON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../test_output'))

# Azure Storage setup
if STORAGE_MODE == 'azure':
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME', 'test-output')
    
    if not AZURE_STORAGE_CONNECTION_STRING:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")
    
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
else:
    JSON_DIR = LOCAL_JSON_DIR

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/files')
def list_files():
    try:
        if STORAGE_MODE == 'azure':
            # List blobs from Azure Storage
            print(f"Connecting to Azure container: {AZURE_CONTAINER_NAME}")
            blobs = container_client.list_blobs()
            files = [blob.name for blob in blobs if blob.name.endswith('.json')]
            print(f"Found {len(files)} files in Azure")
        else:
            # List files from local directory
            print(f"Reading from local directory: {LOCAL_JSON_DIR}")
            if not os.path.exists(LOCAL_JSON_DIR):
                print(f"Directory does not exist: {LOCAL_JSON_DIR}")
                return jsonify({'error': f'Directory not found: {LOCAL_JSON_DIR}'}), 404
            files = [f for f in os.listdir(LOCAL_JSON_DIR) if f.endswith('.json')]
            print(f"Found {len(files)} files locally")
        
        return jsonify(sorted(files))
    except Exception as e:
        print(f"Error listing files: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/file/<filename>')
def get_file(filename):
    try:
        if STORAGE_MODE == 'azure':
            # Read blob from Azure Storage
            blob_client = container_client.get_blob_client(filename)
            blob_data = blob_client.download_blob().readall()
            data = json.loads(blob_data)
        else:
            # Read file from local directory
            file_path = os.path.join(LOCAL_JSON_DIR, filename)
            if not os.path.isfile(file_path):
                return jsonify({'error': 'File not found'}), 404
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Extract all 'fields' objects from result.contents
        result = data.get('result', {})
        contents = result.get('contents', [])
        fields_list = []
        
        for item in contents:
            fields = item.get('fields')
            if fields:
                # Get company name from fields
                company_name = 'Unknown'
                if fields.get('Name_of_Company', {}).get('valueString'):
                    company_name = fields['Name_of_Company']['valueString']
                
                # Convert fields object to a list of key-value pairs for better display
                fields_dict = {
                    'company_name': company_name,
                    'fields': fields,
                    'kind': item.get('kind', 'N/A')
                }
                fields_list.append(fields_dict)
        
        return jsonify(fields_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
