import requests
from typing import Optional, List, Dict
import config


def get_system_prompt(mode: str) -> Optional[str]:
    """Get system prompt based on mode."""
    prompts = {
        "WITHOUT_CONTEXT": None,
        "CAD": "You are a helpful CAD assistant.",
        "RAG": "You are an AI assistant that answers questions based on provided context about EORA company projects."
    }
    return prompts.get(mode)


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