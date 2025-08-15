import requests
import json
import os
from typing import Optional, List, Dict
import config


def load_response_instructions() -> str:
    """Load response format instructions."""
    instructions_path = os.path.join(config.PROJECT_ROOT, "prompts", "response_instructions.txt")
    try:
        with open(instructions_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""


def load_knowledge_base() -> str:
    """Load knowledge base as JSON string."""
    try:
        with open(config.PARSED_DATA_PATH, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
            return json.dumps(knowledge_base, ensure_ascii=False, indent=2)
    except:
        return "[]"


def get_system_prompt(mode: str) -> Optional[str]:
    """Get system prompt based on mode."""
    if mode == "WITHOUT_CONTEXT":
        return None
    elif mode == "CAD":
        instructions = load_response_instructions()
        knowledge_base = load_knowledge_base()
        return f"""{instructions}

БАЗА ЗНАНИЙ EORA (JSON):
{knowledge_base}

Используйте эту информацию для ответов на вопросы пользователей."""
    elif mode == "RAG":
        return None
    
    return None


def send_message_to_llm(message: str, mode: str = None) -> Optional[str]:
    """Send message to OpenRouter DeepSeek with system prompt."""
    if mode is None:
        mode = config.LLM_MODE
    
    messages = []
    
    # Add system prompt if exists
    system_prompt = get_system_prompt(mode)
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add user message
    messages.append({"role": "user", "content": message})
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": config.LLM_MODEL,
                "messages": messages,
                "max_tokens": config.MAX_TOKENS,
                "temperature": config.TEMPERATURE
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            print(f"LLM API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"LLM error: {e}")
        return None