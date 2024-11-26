import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Diretório base (onde está o arquivo config.py)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Caminho absoluto para a pasta src/uploads
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../../uploads/')
