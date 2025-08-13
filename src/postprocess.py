import json
import re
from typing import List, Dict


def clean_json_garbage(text: str) -> str:
    """Remove JSON form data garbage from text."""
    # Remove JSON-like structures with li_ prefixes
    pattern = r'\[?\{\"lid.*?\}\]?\s*'
    text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    # Remove other JSON patterns
    pattern = r'\[?\{["\'][\w_]+["\']:["\'].*?\}[,\]]?\s*'
    text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    return text


def find_common_endings(texts: List[str]) -> str:
    """Find common ending across all texts."""
    if len(texts) < 2:
        return ""
    
    # Get last 500 chars from each text
    endings = [text[-500:] for text in texts if len(text) > 100]
    
    if not endings:
        return ""
    
    # Find longest common suffix
    common_ending = ""
    min_length = min(len(ending) for ending in endings)
    
    for i in range(1, min_length):
        suffix = endings[0][-i:]
        if all(ending.endswith(suffix) for ending in endings):
            if len(suffix) > len(common_ending):
                common_ending = suffix
    
    # Only return if common ending is substantial (>50 chars)
    return common_ending if len(common_ending) > 50 else ""


def remove_duplicate_endings(knowledge_base: List[Dict[str, str]]) -> None:
    """Remove common endings from all texts."""
    texts = [entry['text'] for entry in knowledge_base if 'text' in entry]
    common_ending = find_common_endings(texts)
    
    if common_ending:
        print(f"Found common ending: {len(common_ending)} chars")
        for entry in knowledge_base:
            if 'text' in entry and entry['text'].endswith(common_ending):
                entry['text'] = entry['text'][:-len(common_ending)].strip()


def postprocess_knowledge_base(input_file: str, output_file: str) -> bool:
    """Clean knowledge base from garbage and duplicates."""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
        
        print(f"Cleaning {len(knowledge_base)} entries")
        
        # Clean JSON garbage from each text
        for entry in knowledge_base:
            if 'text' in entry:
                entry['text'] = clean_json_garbage(entry['text'])
        
        # Remove common endings across all texts
        remove_duplicate_endings(knowledge_base)
        
        # Final cleanup
        for entry in knowledge_base:
            if 'text' in entry:
                original_length = len(entry['text'])
                entry['text'] = re.sub(r'\s+', ' ', entry['text']).strip()
                new_length = len(entry['text'])
                print(f"Cleaned text: {original_length} -> {new_length} chars")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
        
        print(f"Saved cleaned data to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error processing: {e}")
        return False