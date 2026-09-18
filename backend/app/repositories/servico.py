from sqlalchemy.orm import Session

from app.models.servico import Servico
from app.schemas.servico import ServicoCreate


def criar_servico(
    db: Session,
    servico: ServicoCreate,
    empresa_id: int,
) -> Servico:
    novo_servico = Servico(
        empresa_id=empresa_id,
        nome=servico.nome,
        descricao=servico.descricao,
        preco_padrao=servico.preco_padrao,
        duracao_minutos=servico.duracao_minutos,
        requer_recurso=servico.requer_recurso,
        tipo_recurso=servico.tipo_recurso,
        modo_selecao_recurso=servico.modo_selecao_recurso,
        ativo=True,
    )

    db.add(novo_servico)
    db.flush()
    return novo_servico


def listar_servicos(
    db: Session,
    empresa_id: int,
    busca: str | None = None,
    ativo: bool | None = None,
    pagina: int = 1,
    limite: int = 10,
) -> list[Servico]:
    query = db.query(Servico).filter(Servico.empresa_id == empresa_id)

    if busca:
        query = query.filter(Servico.nome.ilike(f"%{busca}%"))

    if ativo is not None:
        query = query.filter(Servico.ativo == ativo)

    return (
        query.order_by(Servico.nome.asc(), Servico.id.asc())
        .offset((pagina - 1) * limite)
        .limit(limite)
        .all()
    )


def buscar_servico_por_id(
    db: Session,
    servico_id: int,
    empresa_id: int,
) -> Servico | None:
    return (
        db.query(Servico)
        .filter(
            Servico.id == servico_id,
            Servico.empresa_id == empresa_id,
        )
        .first()
    )


def atualizar_servico(
    db: Session,
    servico_db: Servico,
    dados: dict,
) -> Servico:
    campos_permitidos = {
        "nome",
        "descricao",
        "preco_padrao",
        "duracao_minutos",
        "requer_recurso",
        "tipo_recurso",
        "modo_selecao_recurso",
        "ativo",
    }

    for campo, valor in dados.items():
        if campo in campos_permitidos:
            setattr(servico_db, campo, valor)

    return servico_db


def desativar_servico(db: Session, servico_db: Servico) -> Servico:
    servico_db.ativo = False
    return servico_db
