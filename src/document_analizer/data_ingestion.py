import os
import fitz
import sys
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exceptions.custom_exceptions import DocumentPortalException

class DocumentHandler:
    """
    Handles PDF saving and reading operations.
    Automatically logs all actions and supports session-based organization.
    """

    def __init__(self, session_id=None, data_dir=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            # self.data_dir = data_dir or os.getenv(
            #     "DATA_STORAGE_PATH",
            #     os.path.join(os.getcwd(), "data", "document_analysis")
            # )

            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.data_dir = data_dir or os.getenv(
            "DATA_STORAGE_PATH",
            os.path.join(project_root, "data", "document_analysis")
       )


            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
            # Create base session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.log.info(f"PDFHandler initialized. session_id={self.session_id}, session_path={self.session_path}")
        except Exception as e:
            self.log.error(f"Error initializing DocumentHandler: {e}")
            raise DocumentPortalException("Error initializing DocumentHandler", sys)

if __name__ == "__main__":
    try:
        handler = DocumentHandler()
        print(f"Session ID: {handler.session_id}")
        print(f"Session Path: {handler.session_path}")
    except DocumentPortalException as e:
        print(f"Initialization failed: {e}")
               

        



     

