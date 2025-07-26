# 📄 LlamaIndex Chat System

This project allows you to chat with documents from different data sources (Google Drive, Google Docs) using LlamaIndex’s **official data connectors** and a modular, protocol-driven architecture.

## 🚀 Features
- Download and index PDF files from Google Drive using `GoogleDriveReader`
- Read and index Google Docs documents using `GoogleDocsReader`
- HuggingFace-based embedding model (BAAI/bge-small-en-v1.5)
- Fast and cost-effective answers with Google Gemini LLM (gemini-1.5-flash)
- Modern, user-friendly chat interface built with Streamlit
- Modular, extensible, and protocol-based architecture

## 📁 Project Structure
```
project/
├── google_drive/          # Google Drive integration
│   ├── embedding_method.py # Uses LlamaIndex GoogleDriveReader
│   └── chat_interface.py
├── google_docs/           # Google Docs integration
│   ├── embedding_method.py # Uses LlamaIndex GoogleDocsReader
│   └── chat_interface.py
├── shared/                # Shared utilities and configuration
│   ├── protocol.py        # EmbeddingMethod protocol
│   ├── llama_utils.py
│   └── config.py
├── main.py                # Main entry point
├── requirements.txt
└── .gitignore
```

## 🏗️ Architecture
- **Official LlamaIndex Readers:**  
  - Google Drive: [`GoogleDriveReader`](https://docs.llamaindex.ai/en/stable/examples/data_connectors/GoogleDriveDemo/)
  - Google Docs: [`GoogleDocsReader`](https://docs.llamaindex.ai/en/stable/examples/data_connectors/GoogleDriveDemo/)
- **Protocol-based:**  
  - All data sources implement the `EmbeddingMethod` protocol for consistency and extensibility.
- **Class-based & Modular:**  
  - Each data source has its own class and folder.
  - Shared logic is in the `shared/` folder.

## ⚡️ Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install llama-index-readers-google
   ```

2. **Google Cloud Setup:**
   - Enable Google Drive and Google Docs APIs.
   - Create an OAuth 2.0 Client ID (Desktop app) and download the credentials as `credentials.json`.
   - Add your Google account as a test user in the OAuth consent screen.
   - Place `credentials.json` in the project root.

3. **Run the app:**
   ```bash
   streamlit run main.py
   ```

4. **In the web interface:**
   - Select your data source (Google Drive or Google Docs)
   - Click “Download & Index PDFs” or “Download & Index Document”
   - Ask questions and chat with your documents!

## 📝 Notes
- Files like `credentials.json`, `drive_downloads/`, and `llama_index_storage/` are excluded from version control via `.gitignore`.
- The project is compatible with Python 3.9+.

## 🤝 Contributing
Contributions and suggestions are welcome!

---

**This project is built with official LlamaIndex connectors and follows a clean, extensible, and professional architecture.** 