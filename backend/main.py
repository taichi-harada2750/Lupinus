from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import uuid
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 将来的に制限してもOK
    allow_methods=["*"],
    allow_headers=["*"],
)
class Bookmark(BaseModel):
    title: str
    url: str
    source: Optional[str] = "manual"
    published: Optional[str] = None
    translated_title: Optional[str] = None


DATA_PATH = Path(__file__).parent / "data.json"

# 最初は空データで保存ファイルを用意
if not DATA_PATH.exists():
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.get("/")
def read_root():
    return {"message": "Lupinus backend running"}

@app.get("/articles")
def get_articles():
    data = load_data()
    return {"articles": data}

@app.post("/bookmark")
async def add_bookmark(bookmark: Bookmark):
    new_article = {
        "id": str(uuid.uuid4()),
        "title": bookmark.title,
        "url": bookmark.url,
        "source": bookmark.source,
        "published": bookmark.published,
        "translated_title": bookmark.translated_title,
        "summary": None,
        "bookmarked": True
    }
    data = load_data()
    data.append(new_article)
    save_data(data)
    return {"message": "bookmarked", "id": new_article["id"]}

