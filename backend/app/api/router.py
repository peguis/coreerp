from fastapi import APIRouter

from app.api.empresa import router as empresa_router
from app.api.usuario import router as usuario_router
from app.api.produto import router as produto_router
from app.api.cliente import router as cliente_router
from app.api.movimento_estoque import router as movimento_estoque_router
from app.api.venda import router as venda_router
from app.api.dashboard import router as dashboard_router
from app.api.produto_imagem import router as produto_imagem_router
from app.api.financeiro import router as financeiro_router
from app.api.categoria_financeira import router as categoria_financeira_router
from app.api.lancamento_financeiro import router as lancamento_financeiro_router

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

router.include_router(
    movimento_estoque_router
)

router.include_router(
    venda_router
)

router.include_router(
    dashboard_router
)

router.include_router(
    produto_imagem_router
)

router.include_router(
    financeiro_router
)

router.include_router(
    categoria_financeira_router
)

router.include_router(
    lancamento_financeiro_router
)