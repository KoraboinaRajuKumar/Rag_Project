import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS

from src.single_document_chat.data_ingestion import SingleDocumentIngestion
from src.single_document_chat.retriver import ConversationalRAG
from utils.model_loader import ModelLoader

FAISS_INDEX_PATH = Path("faiss_index")

class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def read(self):
        with open(self._file_path, "rb") as f:
            return f.read()

def test_conversational_rag_on_pdf(pdf_path: str, question: str):
    try:
        model_loader = ModelLoader()
        embeddings = model_loader.load_embeddings()
        
        if FAISS_INDEX_PATH.exists() and (FAISS_INDEX_PATH / "index.faiss").exists():
            print("Loading existing FAISS index...")
            try:
                vectorstore = FAISS.load_local(
                    folder_path=str(FAISS_INDEX_PATH), 
                    embeddings=embeddings, 
                    allow_dangerous_deserialization=True
                )
            except TypeError:
                vectorstore = FAISS.load_local(str(FAISS_INDEX_PATH), embeddings=embeddings)

            retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        else:
            print("FAISS index not found. Ingesting PDF and creating index...")
            dummy_file = DummyFile(pdf_path)
            ingestor = SingleDocumentIngestion()
            retriever = ingestor.ingest_files([dummy_file])
            # Save vectorstore if needed inside ingestion class or adjust ingestion to return vectorstore too
            # For now, just save the FAISS index folder by calling the appropriate method if available
            # Example: ingestor.vector_store.save_local(str(FAISS_INDEX_PATH))
        
        print("Running Conversational RAG...")
        session_id = "test_conversational_rag"
        rag = ConversationalRAG(retriever=retriever, session_id=session_id)
        response = rag.invoke(question)
        print(f"\nQuestion: {question}\nAnswer: {response}")
                    
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    pdf_path = "data\\single_document_chat\\sample.pdf"
    question = "What is the Reward Modeling?"

    if not Path(pdf_path).exists():
        print(f"PDF file does not exist at: {pdf_path}")
        sys.exit(1)
    
    test_conversational_rag_on_pdf(pdf_path, question)
