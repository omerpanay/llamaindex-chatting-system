import streamlit as st
from google_drive.chat_interface import run_drive_chat
from google_docs.chat_interface import run_docs_chat

def main():
    st.set_page_config(
        page_title="LlamaIndex Chat System",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 LlamaIndex Chat System")
    st.write("Farklı veri kaynaklarından chat yapabilirsiniz.")
    
    # Sidebar'da kaynak seçimi
    st.sidebar.title("📚 Veri Kaynağı Seçin")
    
    source = st.sidebar.selectbox(
        "Hangi kaynaktan chat yapmak istiyorsunuz?",
        ["Google Drive", "Google Docs"]
    )
    
    # Seçilen kaynağa göre chat arayüzünü çalıştır
    if source == "Google Drive":
        run_drive_chat()
    elif source == "Google Docs":
        run_docs_chat()
    else:
        st.error("Geçersiz kaynak seçimi!")

if __name__ == "__main__":
    main() 