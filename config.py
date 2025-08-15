"""
Конфигурационный файл для проекта RAG-чатбота EORA.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Пути к файлам проекта
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
TASK_LIST_PATH = os.path.join(DOCS_DIR, "task_list.md")
LINK_LIST_PATH = os.path.join(DOCS_DIR, "link_list.txt")
DATABASE_DIR = os.path.join(PROJECT_ROOT, "simple_database")
PARSED_DATA_PATH = os.path.join(DATABASE_DIR, "parsed_list.json")

# Настройки парсинга
# Если None - парсить все ссылки, иначе ограничить количество
PARSING_LIMIT = 2  # Для тестирования установлено ограничение в 2 ссылки

# Настройки веб-парсера
REQUEST_TIMEOUT = 30  # Таймаут для HTTP запросов в секундах
REQUEST_DELAY = 1     # Задержка между запросами в секундах

# LLM настройки
LLM_MODEL = "deepseek/deepseek-r1-0528:free"
LLM_MODE = "WITHOUT_CONTEXT"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настройки для создания директорий
os.makedirs(DATABASE_DIR, exist_ok=True)