"""
Tool for reading and parsing documents from Google Drive.
"""
import os
import logging
from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import json

logger = logging.getLogger("vox")

class GDriveReader:
    def __init__(self):
        self.creds = Credentials.from_authorized_user_info(
            info=json.loads(os.getenv("GOOGLE_CREDS")),
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        self.service = build('drive', 'v3', credentials=self.creds)
        
    def read_document(self, doc_id: str) -> Optional[str]:
        """
        Read and parse a document from Google Drive.
        
        Args:
            doc_id: Google Drive file ID
            
        Returns:
            Parsed content of the document
        """
        try:
            file = self.service.files().get(fileId=doc_id).execute()
            request = self.service.files().export_media(
                fileId=doc_id,
                mimeType='text/plain'
            )
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
            return fh.getvalue().decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error reading document {doc_id}: {str(e)}")
            return None 