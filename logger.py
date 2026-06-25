import logging
import sys
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Suppress verbose dependency debug loops
logging.getLogger("google.genai").setLevel(logging.WARNING)
logger = logging.getLogger("JarvisLogger")