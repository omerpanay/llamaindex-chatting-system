from typing import Sequence, List
from shared.protocol import EmbeddingMethod
from llama_index.core.schema import Document, BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.google import GoogleDocsReader
import multiprocessing
import os

class GoogleDocsEmbeddingMethod(EmbeddingMethod):
    """Embedding method for Google Docs documents"""

    def __init__(self, doc_ids: List[str], credentials_path: str = None):
        self.doc_ids = doc_ids
        self.credentials_path = credentials_path or "credentials.json"

    @staticmethod
    def customize_metadata(document: Document, data_source_id: str, **kwargs) -> Document:
        document.metadata = {
            "title": document.metadata.get("title", ""),
            "data_source": data_source_id,
            "source_type": "google_docs"
        }
        return document

    def get_documents(self, data_source_id: str = "google_docs") -> Sequence[Document]:
        """Get documents from Google Docs"""
        try:
            # Set credentials path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
            print(f"[LOG] (Docs) Using credentials: {self.credentials_path}")
            # Explicitly pass service_account_key to GoogleDocsReader
            reader = GoogleDocsReader(service_account_key=self.credentials_path)
            print(f"[LOG] (Docs) Reader created with service_account_key.")
            # Load documents from Google Docs
            documents = reader.load_data(document_ids=self.doc_ids)
            print(f"[LOG] (Docs) Documents loaded: {len(documents) if documents else 0}")
            # Customize metadata for each document
            for doc in documents:
                self.customize_metadata(doc, data_source_id)
            return documents
        except Exception as e:
            print(f"Error loading documents from Google Docs: {e}")
            return []

    def download_and_process(self) -> Sequence[Document]:
        """Download and process documents from Google Docs"""
        return self.get_documents()

    def create_nodes(self, documents: Sequence[Document]) -> List[BaseNode]:
        """Create nodes from documents"""
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=1024, chunk_overlap=20)
            ]
        )
        nodes = pipeline.run(documents=documents)
        return nodes

    def process(
        self,
        documents: Sequence[Document],
        data_source_id: str = "google_docs"
    ) -> List[BaseNode]:
        """Process documents and create nodes"""
        # Customize metadata for each document
        for doc in documents:
            self.customize_metadata(doc, data_source_id)
        
        # Create nodes
        return self.create_nodes(documents) 