from fastapi import APIRouter

from app.api.empresa import router as empresa_router
from app.api.usuario import router as usuario_router
from app.api.produto import router as produto_router
from app.api.cliente import router as cliente_router

router = APIRouter()


router.include_router(
    empresa_router
)

router.include_router(
    usuario_router
)

router.include_router(
    produto_router
)

router.include_router(
    cliente_router
)