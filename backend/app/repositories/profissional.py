from sqlalchemy.orm import Session

from app.models.profissional import Profissional
from app.models.usuario import Usuario


def criar_profissional(
    db: Session,
    empresa_id: int,
    usuario_id: int,
    area_atuacao: str,
    percentual_padrao,
) -> Profissional:
    profissional = Profissional(
        empresa_id=empresa_id,
        usuario_id=usuario_id,
        area_atuacao=area_atuacao,
        percentual_padrao=percentual_padrao,
        ativo=True,
    )
    db.add(profissional)
    db.flush()
    return profissional


def buscar_profissional_por_id(
    db: Session,
    profissional_id: int,
    empresa_id: int,
) -> Profissional | None:
    return (
        db.query(Profissional)
        .filter(
            Profissional.id == profissional_id,
            Profissional.empresa_id == empresa_id,
        )
        .first()
    )


def buscar_profissional_por_usuario(
    db: Session,
    usuario_id: int,
    empresa_id: int,
) -> Profissional | None:
    return (
        db.query(Profissional)
        .filter(
            Profissional.usuario_id == usuario_id,
            Profissional.empresa_id == empresa_id,
        )
        .first()
    )


def listar_profissionais(
    db: Session,
    empresa_id: int,
    ativo: bool | None = None,
    area_atuacao: str | None = None,
    busca: str | None = None,
    pagina: int = 1,
    limite: int = 10,
) -> list[Profissional]:
    query = (
        db.query(Profissional)
        .join(
            Usuario,
            (Usuario.id == Profissional.usuario_id)
            & (Usuario.empresa_id == Profissional.empresa_id),
        )
        .filter(Profissional.empresa_id == empresa_id)
    )

    if ativo is not None:
        query = query.filter(Profissional.ativo == ativo)

    if area_atuacao:
        query = query.filter(Profissional.area_atuacao == area_atuacao)

    if busca:
        query = query.filter(Usuario.nome.ilike(f"%{busca}%"))

    return (
        query.order_by(Usuario.nome.asc(), Profissional.id.asc())
        .offset((pagina - 1) * limite)
        .limit(limite)
        .all()
    )


def atualizar_profissional(
    db: Session,
    profissional_db: Profissional,
    dados: dict,
) -> Profissional:
    campos_permitidos = {
        "area_atuacao",
        "percentual_padrao",
        "ativo",
    }
    for campo, valor in dados.items():
        if campo in campos_permitidos:
            setattr(profissional_db, campo, valor)
    return profissional_db


def desativar_profissional(
    db: Session,
    profissional_db: Profissional,
) -> Profissional:
    profissional_db.ativo = False
    return profissional_db
