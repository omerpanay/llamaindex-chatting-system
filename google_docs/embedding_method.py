from typing import Sequence, List
from shared.protocol import EmbeddingMethod
from llama_index.core.schema import Document, BaseNode
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.google import GoogleDocsReader
import multiprocessing

class GoogleDocsEmbeddingMethod(EmbeddingMethod):
    """Embedding method for Google Docs documents"""

    def __init__(self, doc_ids: List[str], credentials_path: str = "credentials.json"):
        self.doc_ids = doc_ids
        self.credentials_path = credentials_path

    @staticmethod
    def customize_metadata(document: Document, data_source_id: str, **kwargs) -> Document:
        document.metadata = {
            "title": document.metadata.get("title", ""),
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
        # Use LlamaIndex's built-in GoogleDocsReader
        try:
            # Pass document_ids as a list, as shown in the documentation
            documents = GoogleDocsReader().load_data(document_ids=self.doc_ids)
            # Check if documents is None or empty
            if documents is None:
                print("Warning: GoogleDocsReader returned None")
                return []
            
            for doc in documents:
                self.customize_metadata(doc, data_source_id)
            return documents
        except Exception as e:
            print(f"Error loading documents from Google Docs: {e}")
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