from fastapi import (
    APIRouter,
    Depends,
    status
)

from sqlalchemy.orm import Session


from app.database import get_db

from app.auth.dependencies import (
    get_current_user
)

from app.auth.tenant import get_empresa_id


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
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(get_current_user)
):

    return listar_lancamentos_service(
        db,
        empresa_id
    )







@router.post(
    "/lancamentos",
    status_code=status.HTTP_201_CREATED
)
def criar_lancamento(
    dados: LancamentoFinanceiroCreate,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(get_current_user)
):

    return criar_lancamento_service(
        db,
        dados,
        empresa_id,
        usuario.id
    )







@router.get(
    "/lancamentos/{lancamento_id}"
)
def buscar_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(get_current_user)
):

    return buscar_lancamento_service(
        db,
        lancamento_id,
        empresa_id
    )







@router.put(
    "/lancamentos/{lancamento_id}"
)
def atualizar_lancamento(
    lancamento_id: int,
    dados: LancamentoFinanceiroUpdate,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(get_current_user)
):

    return atualizar_lancamento_service(
        db,
        lancamento_id,
        empresa_id,
        dados
    )







@router.delete(
    "/lancamentos/{lancamento_id}"
)
def excluir_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db),
    empresa_id: int = Depends(get_empresa_id),
    usuario=Depends(get_current_user)
):

    deletar_lancamento_service(
        db,
        lancamento_id,
        empresa_id
    )


    return {
        "mensagem": "Lançamento removido"
    }