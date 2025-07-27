import os

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api import router as api_router
from .core.settings import settings

static_path = os.path.join(os.path.dirname(__file__), "..", "static")

app = FastAPI(
    title='Медицинский Урологический Центр API',
    description='API для системы записи на прием в урологическую клинику',
    version='1.0.0',
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory=static_path), name="static")

app.include_router(
    api_router
)

@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse(os.path.join(static_path, "index.html"))
