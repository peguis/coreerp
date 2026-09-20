from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import require_perfil
from app.database import get_db
from app.schemas.empresa import MatrizDemonstracaoCreate
from app.schemas.matriz import (
    MatrizAuditoriaResponse,
    MatrizDashboardResponse,
    MatrizIdentidadeUpdate,
    MatrizModuloCatalogo,
    MatrizModuloStatusUpdate,
    MatrizUsuarioUpdate,
    MatrizTenantDetalhe,
    MatrizTenantResumo,
    MatrizAprovarConversao,
    MatrizInteracaoCreate,
    MatrizOportunidadeCreate,
    MatrizOportunidadeResponse,
    MatrizOportunidadeUpdate,
    MatrizPreviaDemonstracaoResponse,
    MatrizVendedorResponse,
)
from app.schemas.usuario import UsuarioResponse
from app.services.matriz import (
    atualizar_identidade_empresa_matriz,
    atualizar_modulo_empresa_matriz,
    listar_auditoria_matriz,
    listar_empresas_matriz,
    obter_dashboard_matriz,
    obter_detalhe_empresa_matriz,
    listar_catalogo_modulos_matriz,
    atualizar_usuario_empresa_matriz,
    atualizar_usuario_matriz,
    listar_usuarios_matriz,
)
from app.services.matriz_comercial import (
    aprovar_conversao_matriz,
    atualizar_oportunidade_matriz,
    criar_demonstracao_matriz,
    criar_oportunidade_matriz,
    listar_oportunidades_matriz,
    listar_vendedores_matriz,
    obter_previa_demonstracao_matriz,
    registrar_interacao_matriz,
    solicitar_conversao_matriz,
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


@router.get("/usuarios", response_model=list[UsuarioResponse])
def usuarios_matriz(
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return listar_usuarios_matriz(db, usuario)


@router.patch("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario_da_matriz(
    usuario_id: int,
    dados: MatrizUsuarioUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return atualizar_usuario_matriz(db, usuario_id, dados, usuario)


@router.get("/auditoria", response_model=list[MatrizAuditoriaResponse])
def auditoria_matriz(
    empresa_id: int | None = Query(default=None),
    acao: str | None = Query(default=None, max_length=50),
    limite: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return listar_auditoria_matriz(db, empresa_id=empresa_id, acao=acao, limite=limite)


@router.get("/vendedores", response_model=list[MatrizVendedorResponse])
def vendedores_matriz(
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return listar_vendedores_matriz(db, usuario)


@router.get("/oportunidades", response_model=list[MatrizOportunidadeResponse])
def oportunidades_matriz(
    busca: str | None = Query(default=None, max_length=150),
    vendedor_id: int | None = Query(default=None),
    status: str | None = Query(default=None, max_length=40),
    proxima_acao: str | None = Query(default=None, max_length=180),
    proximo_contato: date | None = Query(default=None),
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return listar_oportunidades_matriz(
        db,
        usuario,
        busca=busca,
        vendedor_id=vendedor_id,
        status=status,
        proxima_acao=proxima_acao,
        proximo_contato=proximo_contato,
    )


@router.post("/oportunidades", response_model=MatrizOportunidadeResponse)
def criar_oportunidade(
    dados: MatrizOportunidadeCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return criar_oportunidade_matriz(db, usuario, dados)


@router.patch("/oportunidades/{oportunidade_id}", response_model=MatrizOportunidadeResponse)
def atualizar_oportunidade(
    oportunidade_id: int,
    dados: MatrizOportunidadeUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return atualizar_oportunidade_matriz(db, usuario, oportunidade_id, dados)


@router.post(
    "/oportunidades/{oportunidade_id}/interacoes",
    response_model=MatrizOportunidadeResponse,
)
def registrar_interacao(
    oportunidade_id: int,
    dados: MatrizInteracaoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return registrar_interacao_matriz(db, usuario, oportunidade_id, dados)


@router.post("/demonstracoes", response_model=MatrizPreviaDemonstracaoResponse)
def criar_demonstracao(
    dados: MatrizDemonstracaoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return criar_demonstracao_matriz(db, usuario, dados)


@router.get(
    "/demonstracoes/{empresa_id}/previa",
    response_model=MatrizPreviaDemonstracaoResponse,
)
def previa_demonstracao(
    empresa_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return obter_previa_demonstracao_matriz(db, usuario, empresa_id)


@router.post(
    "/oportunidades/{oportunidade_id}/solicitar-conversao",
    response_model=MatrizOportunidadeResponse,
)
def solicitar_conversao(
    oportunidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin", "vendedor_pegs")),
):
    return solicitar_conversao_matriz(db, usuario, oportunidade_id)


@router.post(
    "/oportunidades/{oportunidade_id}/aprovar-conversao",
    response_model=MatrizOportunidadeResponse,
)
def aprovar_conversao(
    oportunidade_id: int,
    dados: MatrizAprovarConversao,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return aprovar_conversao_matriz(db, usuario, oportunidade_id, dados)
