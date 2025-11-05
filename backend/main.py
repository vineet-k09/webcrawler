from fastapi import FastAPI, Body, Query, Request
from crawler.crawler import crawl_page
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Web Crawler API")

@app.get("/")
def root():
    return {"message": "Crawler backend running!"}

@app.post("/start")
def start_crawl(request: Request, url: str = Body(None, embed=True), q: str = Query(None)):
    """
    Trigger a crawl on the url if given or take the default from .env.
    Accepts URL either as JSON body {"url": "..."} (embed=True) or as query param ?q=...
    """
    # prefer body url, then query param, then a DEFAULT_URL env var
    base_url = url or q or os.getenv("DEFAULT_URL")
    storage_dir = os.getenv("STORAGE_DIR") or "storage"

    if not base_url:
        return {"error": "No URL provided"}
    
    result = crawl_page(base_url, storage_dir)
    return {"status": "completed", "result": result}