# Кратко по заданию:
- lmm через openrouter - deepseek, асинхронный парсинг ссылок, общение через телеграм, CAD.
- Все сработало, были небольшие проблемы с openrouter и форматированием в телеграме.
- Как mvp сойдет, но нужны тесты. 
- Добавил бы      
  - нужно внедрить тесты; 
  - добавил бы RAG вместо CAD; 
  - нужны сценарии использования бота; 
  - сейчас не совсем четкое следование инструкциям по заданию
  - при большой базе можно пересмотреть подходы к llm


# EORA RAG Chatbot

RAG-powered Telegram chatbot for EORA company that answers questions about projects using website content as knowledge base.

## Features

- **LLM Integration**: Uses OpenRouter API (DeepSeek model)
- **Knowledge Base**: Parses EORA case studies from website
- **Three Difficulty Modes**: Easy, Medium (with sources), Hard (inline citations)
- **Telegram Bot**: Clean HTML formatting with clickable links

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run**:
   ```bash
   python main.py
   ```

## Configuration

- `DIFFICULTY_MODE`: `easy`, `medium`, `hard` (response complexity)
- `LLM_MODE`: `CAD` (with context), `WITHOUT_CONTEXT`, `RAG` (not implemented)
- Change settings in `config.py`

## Architecture

- `src/parser.py` - Web scraping and knowledge base creation
- `src/llm_client.py` - OpenRouter API integration
- `src/telegram_bot.py` - Telegram bot interface
- `src/postprocess.py` - Text formatting and cleanup
- `simple_database/` - JSON knowledge base storage

## Security

- Environment variables for API keys
- Input validation and sanitization
- HTML escaping for Telegram
- URL validation for links

## Notes

- RAG mode is currently not implemented (use CAD mode instead)
- All knowledge base content is loaded into system prompt
