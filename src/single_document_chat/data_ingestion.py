import uuid
from pathlib import Path
from datetime import datetime
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exceptions.custom_exceptions import DocumentPortalException
from utils.model_loader import ModelLoader

class SingleDocumentIngestion:
    def __init__(self,data_dir:str="data/single_document_chat",fiass_dir:str="faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = Path(data_dir)
            self.faiss_dir = Path(fiass_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            self.loader = ModelLoader()
            #self.embedding_model = self.loader.load_embeddings()
            self.log.info(f"SingleDocumentIngestion initialized. data_dir={self.data_dir}, faiss_dir={self.faiss_dir}")
        except Exception as e:
            self.log.error(f"Error initializing SingleDocumentIngestion: {e}")
            raise DocumentPortalException(f"Error initializing SingleDocumentIngestion: {e}") from e
        

    def ingest_files(self,uploaded_files):   # Loading the documents

        try:
            documents=[]
            for uploaded_file in uploaded_files:
                unique_file_name= f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{uploaded_file.name}"
                temp_path=self.data_dir/unique_file_name
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                self.log.info(f"File saved temporarily for ingestion. file={unique_file_name}, path={temp_path}")
                loader=PyPDFLoader(str(temp_path))
                docs=loader.load()
                documents.extend(docs)
            self.log.info(f"Total documents loaded: {len(documents)}") 
            return self._create_retriver(documents)
        except Exception as e:
            self.log.error(f"Error loading documents: {e}")
            raise DocumentPortalException(f"Error loading documents: {e}") from e  
    
    def _create_retriver(self,documents):
        try:
           spliter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
           chunks=spliter.split_documents(documents)
           self.log.info(f"Documents split into chunks. Total chunks created: {len(chunks)}")

           embedding_model = self.loader.load_embeddings()
           vector_store=FAISS.from_documents(documents=chunks, embedding=embedding_model)

           retriver= vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})
           self.log.info("Retriever created successfully with top 3 similar documents.",retriever_type=str(type(retriver)))
           return retriver
        except Exception as e:
            self.log.error(f"Error creating retriever: {e}")
            raise DocumentPortalException(f"Error creating retriever: {e}") from e


           






                    


            
        
    





