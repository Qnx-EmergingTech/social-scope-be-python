import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = os.getenv("LOG_FILE", "app.log")

# Create a rotating file handler
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=2)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)

# Logger for the app
logger = logging.getLogger("social_scope")
logger.setLevel(logging.INFO)
logger.addHandler(handler)