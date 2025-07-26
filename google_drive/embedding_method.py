from typing import Sequence, List
from shared.protocol import EmbeddingMethod
from llama_index.core.schema import Document, BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.google import GoogleDriveReader
from llama_index.core import SimpleDirectoryReader
import multiprocessing
import os

class GoogleDriveEmbeddingMethod(EmbeddingMethod):
    """Embedding method for Google Drive folders"""

    def __init__(self, folder_id: str, credentials_path: str = "credentials.json"):
        self.folder_id = folder_id
        self.credentials_path = credentials_path

    @staticmethod
    def customize_metadata(document: Document, data_source_id: str, **kwargs) -> Document:
        document.metadata = {
            "file_name": document.metadata.get("file_name", ""),
            "data_source_id": data_source_id,
        }
        return document

    def apply_rules(
        self,
        documents: Sequence[Document],
        inclusion_rules: List[str],
        exclusion_rules: List[str],
    ) -> Sequence[Document]:
        # You can apply inclusion/exclusion rules here
        return documents

    def get_documents(self, data_source_id: str) -> List[Document]:
        # Use LlamaIndex's built-in GoogleDriveReader
        try:
            # Pass folder_id as a string, not a list (based on error message)
            documents = GoogleDriveReader().load_data(folder_id=self.folder_id)
            # Check if documents is None or empty
            if documents is None:
                print("Warning: GoogleDriveReader returned None")
                return []
            
            for doc in documents:
                self.customize_metadata(doc, data_source_id)
            return documents
        except Exception as e:
            print(f"Error loading documents from Google Drive: {e}")
            return []

    def get_nodes(self, documents: Sequence[Document]) -> Sequence[BaseNode]:
        pipeline = IngestionPipeline(
            transformations=[
                SentenceSplitter(chunk_size=512, chunk_overlap=20)
            ]
        )
        num_workers = multiprocessing.cpu_count()
        return pipeline.run(documents=documents, num_workers=num_workers)

    def process(
        self,
        vector_store,
        task_manager,
        data_source_id: str,
        task_id: str,
        **kwargs,
    ) -> None:
        pass 