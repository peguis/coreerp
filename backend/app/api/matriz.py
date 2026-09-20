from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_perfil
from app.database import get_db
from app.schemas.matriz import (
    MatrizAuditoriaResponse,
    MatrizDashboardResponse,
    MatrizIdentidadeUpdate,
    MatrizModuloCatalogo,
    MatrizModuloStatusUpdate,
    MatrizUsuarioUpdate,
    MatrizTenantDetalhe,
    MatrizTenantResumo,
)
from app.services.matriz import (
    atualizar_identidade_empresa_matriz,
    atualizar_modulo_empresa_matriz,
    listar_auditoria_matriz,
    listar_empresas_matriz,
    obter_dashboard_matriz,
    obter_detalhe_empresa_matriz,
    listar_catalogo_modulos_matriz,
    atualizar_usuario_empresa_matriz,
)


router = APIRouter(prefix="/matriz", tags=["Matriz Pegs"])


@router.get("/dashboard", response_model=MatrizDashboardResponse)
def dashboard_matriz(
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return obter_dashboard_matriz(db)


@router.get("/modulos/catalogo", response_model=list[MatrizModuloCatalogo])
def catalogo_modulos_matriz(
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return listar_catalogo_modulos_matriz(db)


@router.get("/empresas", response_model=list[MatrizTenantResumo])
def empresas_matriz(
    busca: str | None = Query(default=None, max_length=100),
    status: str | None = Query(default=None, pattern="^(ativo|inativo)$"),
    tipo_negocio: str | None = Query(default=None, max_length=80),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return listar_empresas_matriz(
        db,
        busca=busca,
        status=status,
        tipo_negocio=tipo_negocio,
    )


@router.get("/empresas/{empresa_id}", response_model=MatrizTenantDetalhe)
def detalhe_empresa_matriz(
    empresa_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return obter_detalhe_empresa_matriz(db, empresa_id)


@router.patch("/empresas/{empresa_id}/identidade", response_model=MatrizTenantResumo)
def identidade_empresa_matriz(
    empresa_id: int,
    dados: MatrizIdentidadeUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return atualizar_identidade_empresa_matriz(db, empresa_id, dados, usuario.id)


@router.patch("/empresas/{empresa_id}/modulos/{codigo}")
def modulo_empresa_matriz(
    empresa_id: int,
    codigo: str,
    dados: MatrizModuloStatusUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return atualizar_modulo_empresa_matriz(db, empresa_id, codigo, dados.ativo, usuario.id)


@router.patch("/empresas/{empresa_id}/usuarios/{usuario_id}")
def usuario_empresa_matriz(
    empresa_id: int,
    usuario_id: int,
    dados: MatrizUsuarioUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return atualizar_usuario_empresa_matriz(
        db,
        empresa_id,
        usuario_id,
        dados,
        usuario.id,
    )


@router.get("/auditoria", response_model=list[MatrizAuditoriaResponse])
def auditoria_matriz(
    empresa_id: int | None = Query(default=None),
    acao: str | None = Query(default=None, max_length=50),
    limite: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return listar_auditoria_matriz(db, empresa_id=empresa_id, acao=acao, limite=limite)
