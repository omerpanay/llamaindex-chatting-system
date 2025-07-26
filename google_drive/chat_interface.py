import streamlit as st
from google_drive.embedding_method import GoogleDriveEmbeddingMethod
from shared.llama_utils import setup_llama_index, create_index_from_documents, create_query_engine, ask_question
from shared.config import DRIVE_FOLDER_ID, setup_environment

def run_drive_chat():
    """Run Google Drive chat interface"""
    setup_environment()
    setup_llama_index()
    
    st.title("📄 Google Drive PDF Chatbot")
    st.write("You can ask questions about PDFs downloaded from Google Drive.")
    
    # Create embedding method
    embedder = GoogleDriveEmbeddingMethod(folder_id=DRIVE_FOLDER_ID)
    
    if "drive_chat_history" not in st.session_state:
        st.session_state["drive_chat_history"] = []
    
    if st.button("📥 Download & Index PDFs"):
        with st.spinner("Downloading and indexing PDFs..."):
            try:
                # Get documents
                documents = embedder.get_documents(data_source_id="google_drive")
                
                if documents:
                    # Create index
                    index = create_index_from_documents(documents)
                    query_engine = create_query_engine(index)
                    
                    st.session_state["drive_query_engine"] = query_engine
                    st.success(f"✅ {len(documents)} documents indexed successfully!")
                else:
                    st.error("❌ No documents found!")
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Chat interface
    if "drive_query_engine" in st.session_state:
        user_input = st.text_input("Type your question:")
        
        if st.button("Send") and user_input:
            with st.spinner("Searching for an answer..."):
                try:
                    response = ask_question(st.session_state["drive_query_engine"], user_input)
                    st.session_state["drive_chat_history"].append((user_input, str(response)))
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        # Chat history
        st.markdown("---")
        st.subheader("Chat History")
        for q, a in st.session_state["drive_chat_history"]:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Bot:** {a}")
    else:
        st.info("👆 Click the button above to download and index PDFs first.") 