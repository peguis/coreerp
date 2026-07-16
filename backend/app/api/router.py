from fastapi import APIRouter

from app.api.empresa import router as empresa_router
from app.api.usuario import router as usuario_router


router = APIRouter()


router.include_router(
    empresa_router
)

router.include_router(
    usuario_router
)