from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = os.environ['GDRIVE_FOLDER_ID']
FILE_NAME = os.environ['BUILD_FILE_NAME']
FILE_PATH = f'build/app/outputs/flutter-apk/{FILE_NAME}'

def upload_file():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

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
    from googleapiclient.http import MediaFileUpload
    upload_file()
