from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .v1 import router as v1_router


router = APIRouter(prefix='/api')

router.include_router(
    v1_router
)