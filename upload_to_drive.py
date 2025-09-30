from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json

SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = os.environ['GDRIVE_FOLDER_ID']
FILE_NAME = os.environ['BUILD_FILE_NAME']
FILE_PATH = f'build/app/outputs/flutter-apk/{FILE_NAME}'

def delete_old_files(service):
    query = f"'{FOLDER_ID}' in parents and name contains '.apk' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print("No old APK files found to delete.")
        return

    for file in files:
        print(f"Deleting old file: {file['name']} ({file['id']})")
        service.files().delete(fileId=file['id']).execute()

def upload_file():
    # OAuth credentials থেকে token load করুন
    creds_data = json.loads(os.environ['GDRIVE_TOKEN'])
    credentials = Credentials(
        token=creds_data['access_token'],
        refresh_token=creds_data.get('refresh_token'),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_data['client_id'],
        client_secret=creds_data['client_secret'],
        scopes=SCOPES
    )
    
    service = build('drive', 'v3', credentials=credentials)

    # আগের APK ফাইলগুলো ডিলিট করো
    delete_old_files(service)

    # নতুন ফাইল আপলোড করো
    file_metadata = {
        'name': FILE_NAME,
        'parents': [FOLDER_ID]
    }

    media = MediaFileUpload(FILE_PATH, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"Uploaded file with ID: {file.get('id')}")

if __name__ == '__main__':
    upload_file()