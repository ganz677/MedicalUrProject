from fastapi import APIRouter
from .appointments.routes import router as appointment_router
from .admin.routes import router as auth_router


router = APIRouter(prefix="/v1")

router.include_router(appointment_router)
router.include_router(auth_router)
