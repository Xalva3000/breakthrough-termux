from pathlib import Path
import logging



BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URL_STORAGE_PATH = BASE_DIR / "short_url_storage.json"
LOG_LEVEL = logging.INFO

# print(BASE_DIR)


