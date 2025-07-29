import streamlit as st
from google_drive.embedding_method import GoogleDriveEmbeddingMethod
from shared.llama_utils import setup_llama_index, create_index_from_documents, create_query_engine, ask_question
from shared.config import DRIVE_FOLDER_ID, setup_environment, get_credentials_path

def run_drive_chat():
    """Run Google Drive chat interface"""
    setup_environment()
    
    # --- Sidebar: API Key, Model, Embedding Seçimi ---
    st.sidebar.subheader("🔑 Gemini API Key")
    gemini_api_key = st.sidebar.text_input(
        "Gemini API Key:",
        type="password",
        value=st.session_state.get('gemini_api_key', ""),
        help="Enter your Gemini API Key (Required)"
    )
    if gemini_api_key:
        st.session_state['gemini_api_key'] = gemini_api_key
        import os
        os.environ['GEMINI_API_KEY'] = gemini_api_key

    st.sidebar.subheader("🤖 Model Seçimi")
    llm_model = st.sidebar.selectbox(
        "LLM Model:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
        index=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"].index(st.session_state.get('llm_model', 'gemini-1.5-flash')) if 'llm_model' in st.session_state else 0
    )
    st.session_state['llm_model'] = llm_model

    embedding_model = st.sidebar.selectbox(
        "Embedding Model:",
        ["BAAI/bge-small-en-v1.5", "BAAI/bge-base-en-v1.5", "BAAI/bge-large-en-v1.5"],
        index=["BAAI/bge-small-en-v1.5", "BAAI/bge-base-en-v1.5", "BAAI/bge-large-en-v1.5"].index(st.session_state.get('embedding_model', 'BAAI/bge-small-en-v1.5')) if 'embedding_model' in st.session_state else 0
    )
    st.session_state['embedding_model'] = embedding_model

    # --- Ana Ekran: Başlık ve Ayarlar ---
    setup_llama_index()
    st.title("📄 Google Drive PDF Chatbot")
    st.write("You can ask questions about PDFs downloaded from Google Drive.")

    # Folder ID input
    st.subheader("📁 Google Drive Folder Settings")
    folder_id = st.text_input(
        "Google Drive Folder ID:",
        value=st.session_state.get('drive_folder_id', ""),
        help="Enter the Google Drive folder ID you want to index"
    )
    if folder_id:
        st.session_state['drive_folder_id'] = folder_id

    # Model configuration display
    st.subheader("🤖 Model Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Embedding Model:** {embedding_model}")
    with col2:
        st.info(f"**LLM Model:** {llm_model}")

    # --- Download & Index ---
    if st.button("📥 Download & Index PDFs", type="primary"):
        try:
            with st.spinner("Downloading and indexing PDFs..."):
                # Get credentials path from session_state (main.py'den geliyor)
                credentials_path = st.session_state.get('credentials_path', None)
                if not credentials_path:
                    st.error("❌ Credentials not found. Please upload your credentials.json from the sidebar.")
                    return

                # Ortam değişkenlerini ayarla
                import os
                os.environ['EMBEDDING_MODEL'] = embedding_model
                os.environ['LLM_MODEL'] = llm_model
                os.environ['GEMINI_API_KEY'] = gemini_api_key

                # Create embedding method
                embedding_method = GoogleDriveEmbeddingMethod(
                    folder_id=folder_id,
                    credentials_path=credentials_path
                )

                # Download and process documents
                documents = embedding_method.download_and_process()

                if documents:
                    # Create index
                    index = create_index_from_documents(documents)

                    # Store in session state
                    st.session_state['drive_index'] = index
                    st.session_state['drive_query_engine'] = create_query_engine(index)

                    st.success(f"✅ Successfully indexed {len(documents)} documents!")
                else:
                    st.error("❌ No documents found in the specified folder.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("Please check your credentials, API key, and folder ID.")

    # --- Chat interface ---
    if 'drive_query_engine' in st.session_state:
        st.subheader("💬 Chat with your documents")

        # Chat input
        user_question = st.text_input(
            "Ask a question about your documents:",
            placeholder="What is this document about?"
        )

        if user_question:
            try:
                with st.spinner("Thinking..."):
                    response = ask_question(st.session_state['drive_query_engine'], user_question)

                st.subheader("🤖 Answer:")
                st.write(response.response)

            except Exception as e:
                st.error(f"❌ Error getting response: {e}")
    else:
        st.info("👆 Click 'Download & Index PDFs' to start chatting with your documents.")