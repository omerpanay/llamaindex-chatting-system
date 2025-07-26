import os

# API Keys
GOOGLE_API_KEY = "AIzaSyD0unaM9Ka92fM5sLNgOxSL5_diWohcAdU"
GOOGLE_APPLICATION_CREDENTIALS = "credentials.json"

# Google Drive Settings
# Make sure this folder ID is correct and accessible
DRIVE_FOLDER_ID = "1zyKR8R9SxhOmp4wCqTlojNb9SZMZJfkF"
DRIVE_DOWNLOAD_DIR = "./drive_downloads"

# Google Docs Settings
DOCS_DOCUMENT_ID = "1sJjoOHvUMwFX7q0iU8aUnOS4d6889QDT_YTernsJgAk"

# LlamaIndex Settings
INDEX_STORAGE_DIR = "llama_index_storage"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "gemini-1.5-flash"

# Environment setup
def setup_environment():
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS 