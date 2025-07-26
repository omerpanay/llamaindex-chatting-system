from googleapiclient.discovery import build
from google.oauth2 import service_account
from shared.config import GOOGLE_APPLICATION_CREDENTIALS

def fetch_google_doc_content(document_id: str, credentials_path: str = GOOGLE_APPLICATION_CREDENTIALS):
    """Fetch content from Google Docs"""
    creds = service_account.Credentials.from_service_account_file(
        credentials_path, 
        scopes=["https://www.googleapis.com/auth/documents.readonly"]
    )
    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().get(documentId=document_id).execute()
    
    content = ""
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            for run in element["paragraph"].get("elements", []):
                if "textRun" in run:
                    content += run["textRun"].get("content", "")
    
    title = doc.get("title", "")
    return title, content 