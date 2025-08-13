"""
Конфигурационный файл для проекта RAG-чатбота EORA.
"""

import os

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

# Настройки для создания директорий
os.makedirs(DATABASE_DIR, exist_ok=True)