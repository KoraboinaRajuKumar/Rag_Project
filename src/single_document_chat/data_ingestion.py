import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from exceptions.custom_exceptions import DocumentPortalException
from utils.model_loader import ModelLoader

class SingleDocumentIngestion:
    def __init__(self, data_dir: str = "data/single_document_chat", faiss_dir: str = "faiss_index"):
        try:
            self.data_dir = Path(data_dir)
            self.faiss_dir = Path(faiss_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            self.loader = ModelLoader()
            self.embedding_model = self.loader.load_embeddings()

            print(f"[INFO] SingleDocumentIngestion initialized. data_dir={self.data_dir}, faiss_dir={self.faiss_dir}")
        except Exception as e:
            print(f"[ERROR] Error initializing SingleDocumentIngestion: {e}")
            raise DocumentPortalException(
                "Error initializing SingleDocumentIngestion",
                error_details=str(e)
            ) from e

    def ingest_files(self, uploaded_files: List[Any]) -> Any:
        """
        uploaded_files: List of file-like objects (must have .name and .read())
        Returns: Retriever object
        """
        try:
            documents = []

            for uploaded_file in uploaded_files:
                # Create a unique filename
                unique_file_name = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{uploaded_file.name}"
                temp_path = self.data_dir / unique_file_name

                # Write uploaded file bytes to disk
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                print(f"[INFO] File saved temporarily: {unique_file_name} at {temp_path}")

                # Load PDF document(s)
                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)

            print(f"[INFO] Total documents loaded: {len(documents)}")
            return self._create_retriever(documents)

        except Exception as e:
            print(f"[ERROR] Error loading documents: {e}")
            raise DocumentPortalException(
                "Error loading documents",
                error_details=str(e)
            ) from e

    def _create_retriever(self, documents: List[Any]) -> Any:
        try:
            # Split documents into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(documents)

            print(f"[INFO] Documents split into chunks. Total chunks created: {len(chunks)}")

            # Load embeddings again (could also reuse self.embedding_model if preferred)
            embedding_model = self.loader.load_embeddings()
            vector_store = FAISS.from_documents(documents=chunks, embedding=embedding_model)

            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

            print(f"[INFO] Retriever created successfully with top 3 similar documents. Retriever type: {type(retriever)}")
            return retriever

        except Exception as e:
            print(f"[ERROR] Error creating retriever: {e}")
            raise DocumentPortalException(
                "Error creating retriever",
                error_details=str(e)
            ) from e
