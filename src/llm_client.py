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


def load_difficulty_examples() -> str:
    """Load difficulty examples based on current difficulty mode."""
    examples_path = os.path.join(config.PROJECT_ROOT, "prompts", "difficulty_examples.json")
    try:
        with open(examples_path, 'r', encoding='utf-8') as f:
            examples = json.load(f)
            current_mode = getattr(config, 'DIFFICULTY_MODE', 'medium')
            if current_mode in examples:
                example_data = examples[current_mode]
                return f"""

RESPONSE FORMAT EXAMPLE ({current_mode.upper()}):
{example_data['description']}

Question: {example_data['example']['question']}
Answer: {example_data['example']['answer']}

Follow this format for all responses."""
    except:
        pass
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
    difficulty_examples = load_difficulty_examples()
    
    if mode == "WITHOUT_CONTEXT":
        return difficulty_examples if difficulty_examples else None
    elif mode == "CAD":
        instructions = load_response_instructions()
        knowledge_base = load_knowledge_base()
        return f"""{instructions}

EORA KNOWLEDGE BASE (JSON):
{knowledge_base}

Use this information to answer user questions.{difficulty_examples}"""
    elif mode == "RAG":
        return difficulty_examples if difficulty_examples else None
    
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