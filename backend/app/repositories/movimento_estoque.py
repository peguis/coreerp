from sqlalchemy.orm import Session

from app.models.movimento_estoque import MovimentoEstoque
from app.schemas.movimento_estoque import MovimentoEstoqueCreate


def criar_movimento(
    db: Session,
    movimento: MovimentoEstoqueCreate,
    empresa_id: int,
    usuario_id: int
):
    novo_movimento = MovimentoEstoque(
        empresa_id=empresa_id,
        produto_id=movimento.produto_id,
        usuario_id=usuario_id,
        tipo=movimento.tipo,
        quantidade=movimento.quantidade,
        observacao=movimento.observacao
    )

    db.add(novo_movimento)
    db.commit()
    db.refresh(novo_movimento)

    return novo_movimento


def listar_movimentos(
    db: Session,
    empresa_id: int
):
    return db.query(MovimentoEstoque).filter(
        MovimentoEstoque.empresa_id == empresa_id
    ).all()


def buscar_movimento_por_id(
    db: Session,
    movimento_id: int,
    empresa_id: int
):
    return db.query(MovimentoEstoque).filter(
        MovimentoEstoque.id == movimento_id,
        MovimentoEstoque.empresa_id == empresa_id
    ).first()