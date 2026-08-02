from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.auth.dependencies import require_perfil

from app.schemas.lancamento_financeiro import (
    LancamentoFinanceiroCreate,
    LancamentoFinanceiroUpdate
)

from app.services.lancamento_financeiro import (
    criar_lancamento_service,
    listar_lancamentos_service,
    buscar_lancamento_service,
    atualizar_lancamento_service,
    deletar_lancamento_service
)


router = APIRouter(
    prefix="/financeiro",
    tags=["Financeiro"]
)



@router.get(
    "/lancamentos"
)
def listar_lancamentos(
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente",
            "operador",
            "consulta"
        )
    )
):

    return listar_lancamentos_service(
        db,
        usuario.empresa_id
    )



@router.post(
    "/lancamentos",
    status_code=status.HTTP_201_CREATED
)
def criar_lancamento(
    dados: LancamentoFinanceiroCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente"
        )
    )
):

    return criar_lancamento_service(
        db,
        dados,
        usuario.empresa_id,
        usuario.id
    )



@router.get(
    "/lancamentos/{lancamento_id}"
)
def buscar_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente",
            "operador",
            "consulta"
        )
    )
):

    return buscar_lancamento_service(
        db,
        lancamento_id,
        usuario.empresa_id
    )



@router.put(
    "/lancamentos/{lancamento_id}"
)
def atualizar_lancamento(
    lancamento_id: int,
    dados: LancamentoFinanceiroUpdate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil(
            "admin",
            "gerente"
        )
    )
):

    return atualizar_lancamento_service(
        db,
        lancamento_id,
        usuario.empresa_id,
        dados
    )



@router.delete(
    "/lancamentos/{lancamento_id}"
)
def excluir_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_perfil(
            "admin"
        )
    )
):

    deletar_lancamento_service(
        db,
        lancamento_id,
        usuario.empresa_id
    )


    return {
        "mensagem": "Lançamento removido"
    }