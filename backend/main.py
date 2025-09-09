# backend/main.py
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = BASE_DIR / "static"                
TEMPLATES_DIR = BASE_DIR / "templates"          

app = FastAPI()


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Если у тебя есть отдельные роуты:
@app.get("/blog", response_class=HTMLResponse)
def serve_blog(request: Request):
    return templates.TemplateResponse("blog-article.html", {"request": request})
