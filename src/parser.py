import json
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Optional


def load_urls(file_path: str) -> List[str]:
    """Load URLs from text file."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


async def parse_page(session: aiohttp.ClientSession, url: str) -> Dict[str, str]:
    """Extract text content from web page."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            response.raise_for_status()
            html = await response.text()
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Extract and clean text
            text = soup.get_text(separator=' ', strip=True)
            text = ' '.join(text.split())  # Remove extra whitespace
            
            if text:
                return {"url": url, "text": text}
            else:
                return {"url": url, "text": ""}
        
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return {"url": url, "text": ""}


async def parse_urls_async(urls: List[str]) -> List[Dict[str, str]]:
    """Parse URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [parse_page(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and empty results
        knowledge_base = []
        for result in results:
            if isinstance(result, dict) and result.get("text"):
                knowledge_base.append(result)
        
        return knowledge_base


async def create_knowledge_base_async(urls_file: str, output_file: str, limit: Optional[int] = None) -> bool:
    """Parse URLs and create knowledge base."""
    urls = load_urls(urls_file)
    
    if limit:
        urls = urls[:limit]
    
    print(f"Parsing {len(urls)} URLs asynchronously...")
    
    # Run async parsing
    knowledge_base = await parse_urls_async(urls)
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"Done. Saved {len(knowledge_base)} pages")
    return len(knowledge_base) > 0


def create_knowledge_base(urls_file: str, output_file: str, limit: Optional[int] = None) -> bool:
    """Parse URLs and create knowledge base (sync wrapper)."""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(create_knowledge_base_async(urls_file, output_file, limit))
    except RuntimeError:
        return asyncio.run(create_knowledge_base_async(urls_file, output_file, limit))