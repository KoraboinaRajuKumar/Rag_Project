import os
import logging
from datetime import datetime

class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Ensure logs directory exists
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Timestamped log file (for persistence)
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir, log_file)
        
        logging.basicConfig(
            filename=self.log_file_path,
            format="[ %(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s",
            level=logging.INFO,
        )

    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)
        return logging.getLogger(logger_name)

# --- Usage Example ---
if __name__ == "__main__":
    logger = CustomLogger().get_logger(__file__)  
    logger.info("This is an info message.")
    logger.info("Hello loges.")