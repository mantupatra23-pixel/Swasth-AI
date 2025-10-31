import logging

logging.basicConfig(
    filename="swasthai_backend.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("SwasthAI")

def log_event(event):
    logger.info(event)
