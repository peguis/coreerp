from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.empresa import (
    EmpresaCreate,
    EmpresaResponse,
    EmpresaConfiguracaoUpdate,
    EmpresaOnboardingResponse,
    EmpresaProvisionamentoCreate,
)

from app.services.empresa import (
    criar_empresa_service,
    buscar_empresa_por_id_service,
    atualizar_empresa_service,
    deletar_empresa_service,
    obter_onboarding_empresa_service,
    provisionar_empresa_service,
)

from app.auth.dependencies import require_perfil
from app.services.auditoria import registrar_auditoria


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)



@router.post(
    "/",
    response_model=EmpresaResponse
)
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil("admin")
    )
):

    return criar_empresa_service(
        db,
        empresa
    )


@router.post(
    "/provisionar",
    response_model=EmpresaResponse,
)
def provisionar_empresa(
    dados: EmpresaProvisionamentoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("pegs_admin")),
):
    return provisionar_empresa_service(db, dados)



@router.get(
    "/me",
    response_model=EmpresaResponse
)
def minha_empresa(
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente", "operador", "consulta"))
):

    empresa = buscar_empresa_por_id_service(
        db,
        usuario.empresa_id
    )


    if not empresa:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )


    return empresa


@router.put(
    "/me/configuracao",
    response_model=EmpresaResponse,
)
def atualizar_minha_configuracao(
    dados: EmpresaConfiguracaoUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente")),
):
    empresa = buscar_empresa_por_id_service(db, usuario.empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    valores = dados.model_dump(exclude_unset=True)
    campos_alterados = sorted(valores.keys())
    if "nome_exibicao" in valores:
        nome = (valores.pop("nome_exibicao") or "").strip()
        if len(nome) < 3:
            raise HTTPException(
                status_code=400,
                detail="O nome exibido deve ter pelo menos 3 caracteres.",
            )
        empresa.nome = nome
    for campo, valor in valores.items():
        if isinstance(valor, str):
            valor = valor.strip() or None
        setattr(empresa, campo, valor)
    registrar_auditoria(
        db,
        empresa_id=usuario.empresa_id,
        usuario_id=usuario.id,
        acao="ATUALIZAR_CONFIGURACAO",
        recurso="empresa",
        recurso_id=empresa.id,
        detalhes={"campos": campos_alterados},
        commit=False,
    )
    db.commit()
    db.refresh(empresa)
    return empresa


@router.get(
    "/me/onboarding",
    response_model=EmpresaOnboardingResponse,
)
def onboarding_minha_empresa(
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente", "operador", "consulta")),
):
    onboarding = obter_onboarding_empresa_service(db, usuario.empresa_id)
    if not onboarding:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return onboarding



@router.get(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
def buscar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_perfil("admin", "gerente", "operador", "consulta"))
):

    if empresa_id != usuario.empresa_id:

        raise HTTPException(
            status_code=403,
            detail="Acesso negado"
        )


    empresa = buscar_empresa_por_id_service(
        db,
        empresa_id
    )


    if not empresa:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )


    return empresa



@router.put(
    "/{empresa_id}",
    response_model=EmpresaResponse
)
def atualizar_empresa(
    empresa_id: int,
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil("admin")
    )
):

    if empresa_id != usuario.empresa_id:

        raise HTTPException(
            status_code=403,
            detail="Acesso negado"
        )


    empresa = buscar_empresa_por_id_service(
        db,
        empresa_id
    )


    if not empresa:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )


    return atualizar_empresa_service(
        db,
        empresa,
        dados
    )



@router.delete(
    "/{empresa_id}"
)
def deletar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil("admin")
    )
):

    if empresa_id != usuario.empresa_id:

        raise HTTPException(
            status_code=403,
            detail="Acesso negado"
        )


    empresa = buscar_empresa_por_id_service(
        db,
        empresa_id
    )


    if not empresa:

        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada"
        )


    deletar_empresa_service(
        db,
        empresa
    )


    return {
        "mensagem": "Empresa removida"
    }
