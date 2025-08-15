from src.llm_client import send_message_to_llm
import config

def test_openrouter():
    """Test OpenRouter connection."""
    print(f"Testing model: {config.LLM_MODEL}")
    
    response = send_message_to_llm("Say 'Hello from DeepSeek!' if you work.")
    
    if response:
        print(f"Success: {response}")
    else:
        print("Failed to connect")

if __name__ == "__main__":
    test_openrouter()