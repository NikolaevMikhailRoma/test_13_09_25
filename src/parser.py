import json
import os
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


def load_urls(file_path: str) -> List[str]:
    """Load URLs from text file."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def parse_page(url: str) -> Optional[str]:
    """Extract text content from web page."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
        
        # Extract and clean text
        text = soup.get_text(separator=' ', strip=True)
        text = ' '.join(text.split())  # Remove extra whitespace
        
        return text if text else None
        
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None


def create_knowledge_base(urls_file: str, output_file: str, limit: Optional[int] = None) -> bool:
    """Parse URLs and create knowledge base."""
    urls = load_urls(urls_file)
    
    if limit:
        urls = urls[:limit]
    
    knowledge_base = []
    
    for i, url in enumerate(urls):
        print(f"Parsing {i+1}/{len(urls)}")
        
        text = parse_page(url)
        if text:
            knowledge_base.append({"url": url, "text": text})
        
        time.sleep(1)  # Rate limiting
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"Done. Saved {len(knowledge_base)} pages")
    return len(knowledge_base) > 0