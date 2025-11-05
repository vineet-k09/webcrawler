# sequntially making the crawler here
# Fetch a page
# Parse links
# Save metadata
# Store HTML to /storage/crawled_pages
# Insert info into SQLite
# Log crawl stats
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

def crawl_page(url: str, storage_dir: str):
    """
    Fetched a page, parses metadata + links, and saves the HTML locally.
    Returns basic crawl info
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}
    
    # parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract metadata
    title = soup.title.string if soup.title else "No title"
    links = [urljoin(url, a.get("href")) for a in soup.find_all("a", href=True)]
    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"])]

    # Save HTML locally
    os.makedirs(storage_dir, exist_ok=True)
    filename = os.path.join(
        storage_dir,
        f"{url.replace('https://','').replace('http://','').replace('/','_')}.html"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.text)

    # Log crawl
    log_entry = f"[{datetime.now()}] Crawled: {url} | Links found: {len(links)}\n"
    os.makedirs("storage/logs", exist_ok=True)
    with open("storage/logs/crawl_log.txt", "a", encoding="utf-8") as log:
        log.write(log_entry)

    # returning results
    return {
        "url": url,
        "title": title,
        "num_links": len(links),
        "headings": headings[:5], 
        "saved_to": filename,
    }