from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = os.environ['GDRIVE_FOLDER_ID']
FILE_NAME = os.environ['BUILD_FILE_NAME']
FILE_PATH = f'build/app/outputs/flutter-apk/{FILE_NAME}'

def delete_old_files(service):
    # আগের ফাইলগুলো খোঁজ এবং ডিলিট করার জন্য কোয়েরি
    query = f"'{FOLDER_ID}' in parents and name contains '.apk'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print("No old APK files found to delete.")
        return

    for file in files:
        print(f"Deleting old file: {file['name']} ({file['id']})")
        service.files().delete(fileId=file['id']).execute()

def upload_file():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
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
