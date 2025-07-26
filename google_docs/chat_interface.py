import streamlit as st
from google_docs.embedding_method import GoogleDocsEmbeddingMethod
from shared.llama_utils import setup_llama_index, create_index_from_documents, create_query_engine, ask_question
from shared.config import DOCS_DOCUMENT_ID, setup_environment

def run_docs_chat():
    """Run Google Docs chat interface"""
    setup_environment()
    setup_llama_index()
    
    st.title("📄 Google Docs Chatbot")
    st.write("You can ask questions about your Google Docs documents.")
    
    # Create embedding method
    embedder = GoogleDocsEmbeddingMethod(doc_ids=[DOCS_DOCUMENT_ID])
    
    if "docs_chat_history" not in st.session_state:
        st.session_state["docs_chat_history"] = []
    
    if st.button("📥 Download & Index Document"):
        with st.spinner("Downloading and indexing document..."):
            try:
                # Get documents
                documents = embedder.get_documents(data_source_id="google_docs")
                
                if documents:
                    # Create index
                    index = create_index_from_documents(documents)
                    query_engine = create_query_engine(index)
                    
                    st.session_state["docs_query_engine"] = query_engine
                    st.success(f"✅ {len(documents)} documents indexed successfully!")
                else:
                    st.error("❌ No documents found!")
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Chat interface
    if "docs_query_engine" in st.session_state:
        user_input = st.text_input("Type your question:")
        
        if st.button("Send") and user_input:
            with st.spinner("Searching for an answer..."):
                try:
                    response = ask_question(st.session_state["docs_query_engine"], user_input)
                    st.session_state["docs_chat_history"].append((user_input, str(response)))
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        # Chat history
        st.markdown("---")
        st.subheader("Chat History")
        for q, a in st.session_state["docs_chat_history"]:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Bot:** {a}")
    else:
        st.info("👆 Click the button above to download and index the document first.") 