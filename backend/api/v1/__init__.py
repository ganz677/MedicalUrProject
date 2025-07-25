from fastapi import APIRouter
from .main_page.routes import router as main_page_router
from .admin_page.routes import router as auth_router


router = APIRouter(
    prefix='/v1'
)

router.include_router(main_page_router)
router.include_router(auth_router)