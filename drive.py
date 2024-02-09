import io
import os
import pickle
import shutil
from mimetypes import MimeTypes

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class Drive:
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self):
        self.creds = None

        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret_.googleusercontent.com.json", self.SCOPES
                )
                self.creds = flow.run_local_server(host="127.0.0.1", port=8000)
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)
        self.service = build("drive", "v3", credentials=self.creds)
        results = (
            self.service.files()
            .list(
                pageSize=100,
                fields="files(id, name)",
            )
            .execute()
        )
        items = results.get("files", [])

        # print("Here's a list of files: \n")
        # print(*items, sep="\n", end="\n\n")

    def download(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        downloader = MediaIoBaseDownload(fh, request, chunksize=204800)
        done = False

        try:
            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)

            with open(file_name, "wb") as f:
                shutil.copyfileobj(fh, f)

            # print("File Downloaded")
            return True
        except:
            print("Something went wrong.")
            return False

   