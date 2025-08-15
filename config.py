"""
Configuration file for EORA RAG chatbot project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Project file paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
TASK_LIST_PATH = os.path.join(DOCS_DIR, "task_list.md")
LINK_LIST_PATH = os.path.join(DOCS_DIR, "link_list.txt")
DATABASE_DIR = os.path.join(PROJECT_ROOT, "simple_database")
PARSED_DATA_PATH = os.path.join(DATABASE_DIR, "parsed_list.json")

# Parsing settings
# If None - parse all links, otherwise limit the number
PARSING_LIMIT = None

# Web parser settings
REQUEST_TIMEOUT = 30  # HTTP request timeout in seconds
REQUEST_DELAY = 1     # Delay between requests in seconds

# LLM settings
LLM_MODEL = "deepseek/deepseek-r1-0528:free"
# Context mode: WITHOUT CONTEXT, CAD, RAG (none active)
LLM_MODE = "CAD"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Response difficulty mode: easy, medium, hard
DIFFICULTY_MODE = "hard"

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Directory creation settings
os.makedirs(DATABASE_DIR, exist_ok=True)