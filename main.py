import streamlit as st
import os
import tempfile
import shutil
from google_drive.chat_interface import run_drive_chat
from shared.config import setup_environment

def handle_credentials_upload():
    """Handle credentials file upload and setup"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Google API Credentials")
    
    uploaded_file = st.sidebar.file_uploader(
        "Upload your credentials.json file",
        type=['json'],
        help="Upload your Google Service Account credentials file"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded credentials as 'credentials.json' in the working directory
            credentials_path = os.path.abspath('credentials.json')
            with open(credentials_path, 'w', encoding='utf-8') as f:
                f.write(uploaded_file.getvalue().decode('utf-8'))

            # Store the credentials path in session state
            st.session_state['credentials_path'] = credentials_path

            # Set environment variable
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

            st.sidebar.success("✅ Credentials uploaded successfully!")
            return True

        except Exception as e:
            st.sidebar.error(f"❌ Error uploading credentials: {e}")
            return False
    
    # Check if credentials are already uploaded
    if 'credentials_path' in st.session_state:
        st.sidebar.success("✅ Credentials already uploaded")
        return True
    
    return False

def cleanup_credentials():
    """Clean up temporary credentials file"""
    if 'credentials_path' in st.session_state:
        try:
            os.unlink(st.session_state['credentials_path'])
            del st.session_state['credentials_path']
        except:
            pass

def main():
    st.set_page_config(
        page_title="LlamaIndex Chat System",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 LlamaIndex Chat System")
    st.write("You can chat with different data sources.")
    
    # Handle credentials upload
    credentials_uploaded = handle_credentials_upload()
    
    if not credentials_uploaded:
        st.warning("⚠️ Please upload your Google API credentials file to continue.")
        st.info("""
        **How to get credentials:**
        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a new project or select existing one
        3. Enable Google Drive API and Google Docs API
        4. Create a Service Account
        5. Download the JSON key file
        6. Upload it here
        """)
        return
    
    # Setup environment
    setup_environment()
    
    # Sidebar: source selection
    st.sidebar.title("📚 Select Data Source")

    # Only Google Drive source selection
    st.sidebar.title("📚 Select Data Source")
    st.sidebar.info("Currently only Google Drive is supported.")
    run_drive_chat()
    
    # Cleanup when app is closed
    if st.sidebar.button("🗑️ Clear Credentials"):
        cleanup_credentials()
        st.rerun()

if __name__ == "__main__":
    main() 