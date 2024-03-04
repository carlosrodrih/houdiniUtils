import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


#drive_folder = "BackupFolder2"
#backup_folder = "backupfiles"
#token_path = "token.json"
#cred_path = "credentials.json"

class gdrive:
	def __init__(self):
		self.creds = None

	def getAuthToken(self,path):
		SCOPES = ["https://www.googleapis.com/auth/drive"]
		cred_path = path + "/credentials.json"
		token_path = path + "/token.json"
		if os.path.exists(token_path):
			self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)

		if not self.creds or not self.creds.valid:
			if self.creds and self.creds.expired and self.creds.refresh_token:
				self.creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(cred_path,SCOPES)
				self.creds = flow.run_local_server(port=0)

			with open(token_path,"w") as token:
				token.write(self.creds.to_json())

	def checkFolder(self, drive_folder):
		try:
			self.service = build("drive","v3",credentials=self.creds)
			response = self.service.files().list(
				q=f"name='{drive_folder}' and mimeType='application/vnd.google-apps.folder'",
				spaces='drive'
			).execute()

			if not response['files']:
				file_metadata = {
				"name": drive_folder,
				 "mimeType":"application/vnd.google-apps.folder"
				}
				file = self.service.files().create(body=file_metadata,fields="id").execute()
				folder_id = file.get('id')
			else:
				folder_id = response['files'][0]['id']

			return folder_id
		except HttpError as e:
			print("Error: "+str(e))

	def uploadFiles(self, folder_id, file_path):
		try:
			file_name = file_path.split("/")[-1]
			file_metadata = {
				"name": file_name,
				"parents": [folder_id] #CARPETA DONDE SE VA A SUBIR
			}
			media = MediaFileUpload(file_path)#PATH DEL ARCHIVO A SUBIR
			upload_file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()

			print("Backed up file: "+ file_name)

		except HttpError as e:
			print("Error: "+str(e))

	def execute(self, path, file_path, drive_folder="HoudiniBackup"):
		self.getAuthToken(path)
		folder_id = self.checkFolder(drive_folder)
		self.uploadFiles(folder_id,file_path)

	def test(self,path):
		print("Test")
		print(path,file)