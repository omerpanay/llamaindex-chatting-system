
# 🤖 LlamaIndex Chat System

A Streamlit-based chatbot system for querying and chatting with documents from Google Drive using LlamaIndex and Gemini LLM.


## 🚀 Features

- **Google Drive Integration**: Download and index PDF files from your Google Drive folder.
- **Secure Credentials Management**: Upload your Google Service Account credentials securely via the web interface.
- **Modern UI**: User-friendly Streamlit web interface.
- **Model Selection**: Choose Gemini LLM and HuggingFace embedding models.
- **Python 3.11 Compatible**: Works best with Python 3.11.


## 📋 Requirements

- Python 3.11 (recommended)
- Google Cloud Project
- Google Drive API enabled
- Service Account credentials (JSON)


## 🛠️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/omerpanay/llamaindex-chatting-system.git
   cd llamaindex-chatting-system
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Google Cloud Setup**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create/select a project
   - Enable Google Drive API
   - Create a Service Account and download the JSON key file


## � Usage

1. **Start the app**
   ```bash
   streamlit run main.py
   ```
2. **Upload credentials**
   - Use the sidebar to upload your `credentials.json` file
3. **Enter Google Drive Folder ID**
   - Input the folder ID you want to index
4. **Select models and index documents**
   - Choose Gemini LLM and embedding model
   - Click "Download & Index PDFs"
5. **Chat with your documents**
   - Ask questions and get answers from your indexed documents


## 📁 Project Structure

```
LlamaIndexing/
├── main.py                 # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
├── .gitignore              # Git ignore file
├── google_drive/           # Google Drive module
│   ├── chat_interface.py   # Drive chat interface
│   ├── embedding_method.py # Drive embedding method
│   └── downloader.py       # File downloader
├── shared/                 # Shared utilities
│   ├── config.py           # Configuration
│   ├── llama_utils.py      # LlamaIndex utilities
│   └── protocol.py         # Protocol definitions
└── llama_index_storage/    # Index storage
```


## 🛠️ Troubleshooting

- **Python Version**: Use Python 3.11 for best compatibility.
- **Credentials**: Make sure your Service Account has the correct permissions and the JSON file is valid.
- **API Limits**: Check Google API quotas if you encounter rate limiting errors.


## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to your branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request