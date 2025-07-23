import os
from google.cloud import translate_v3 as translate
from google.oauth2 import service_account


# Look for .json files in the current directory
json_files = [f for f in os.listdir(".") if f.endswith(".json")]

if len(json_files) != 1:
    raise FileNotFoundError(f"Expected exactly one JSON file, found {len(json_files)}: {json_files}")

SERVICE_ACCOUNT_KEY_PATH = json_files[0] 
LOCATION = 'global'
# Load credentials from the service account JSON file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_KEY_PATH
)

# Get the project ID from the loaded credentials
project_id = credentials.project_id
if not project_id:
    raise ValueError("Project ID not found in service account key file.")

client = translate.TranslationServiceClient(credentials=credentials)
parent = f"projects/{project_id}/locations/{LOCATION}"