import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Detecta se está rodando como EXE ou script
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Carrega .env externo se existir
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

EXCEL_FILE = os.getenv("EXCEL_FILE", str(DATA_DIR / "Renovacao.xlsx"))
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "BR")
MINUTES_BETWEEN_MESSAGES = int(os.getenv("MINUTES_BETWEEN_MESSAGES", 1))
WAIT_TIME = int(os.getenv("WAIT_TIME", 10))
CLOSE_TIME = int(os.getenv("CLOSE_TIME", 3))

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_SMTP = os.getenv("EMAIL_SMTP", "smtp.locaweb.com.br")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
