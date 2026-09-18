from decimal import Decimal, InvalidOperation

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.enums import ModoReservaRecurso
from app.repositories.servico import (
    atualizar_servico,
    buscar_servico_por_id,
    criar_servico,
    desativar_servico,
    listar_servicos,
)


def _validar_nome(nome: str | None) -> str:
    if not isinstance(nome, str):
        raise HTTPException(
            status_code=400,
            detail="O nome do servico e obrigatorio.",
        )

    nome_normalizado = nome.strip()
    if not nome_normalizado:
        raise HTTPException(
            status_code=400,
            detail="O nome do servico nao pode ser vazio.",
        )

    return nome_normalizado


def _validar_preco(preco) -> None:
    try:
        valor = Decimal(str(preco))
    except (InvalidOperation, TypeError, ValueError):
        valor = None

    if valor is None or not valor.is_finite() or valor < 0:
        raise HTTPException(
            status_code=400,
            detail="O preco_padrao nao pode ser negativo.",
        )


def _normalizar_tipo_recurso(tipo):
    if tipo is None:
        return None
    if not isinstance(tipo, str) or not tipo.strip():
        raise HTTPException(
            status_code=400,
            detail="O tipo_recurso deve ser informado quando necessario.",
        )
    return tipo.strip().upper()


def _normalizar_categoria(categoria):
    if categoria is None:
        return None
    if not isinstance(categoria, str) or not categoria.strip():
        raise HTTPException(
            status_code=400,
            detail="A categoria deve ser informada ou deixada vazia.",
        )
    return categoria.strip()


def criar_servico_service(
    db: Session,
    servico,
    empresa_id: int,
):
    servico.nome = _validar_nome(servico.nome)
    servico.categoria = _normalizar_categoria(servico.categoria)
    _validar_preco(servico.preco_padrao)
    servico.tipo_recurso = _normalizar_tipo_recurso(servico.tipo_recurso)
    servico.modo_selecao_recurso = ModoReservaRecurso(
        servico.modo_selecao_recurso
    ).value
    if servico.requer_recurso and not servico.tipo_recurso:
        raise HTTPException(
            status_code=400,
            detail="O tipo_recurso e obrigatorio quando o servico exige recurso.",
        )
    if servico.requer_recurso and not servico.modo_selecao_recurso:
        raise HTTPException(
            status_code=400,
            detail="O modo de selecao do recurso e obrigatorio.",
        )

    try:
        novo_servico = criar_servico(db, servico, empresa_id)
        db.commit()
        db.refresh(novo_servico)
        return novo_servico
    except Exception:
        db.rollback()
        raise


def listar_servicos_service(
    db: Session,
    empresa_id: int,
    busca: str | None = None,
    ativo: bool | None = None,
    pagina: int = 1,
    limite: int = 10,
):
    if pagina < 1 or limite < 1:
        raise HTTPException(
            status_code=400,
            detail="Pagina e limite devem ser maiores que zero.",
        )

    return listar_servicos(
        db,
        empresa_id,
        busca.strip() if busca else None,
        ativo,
        pagina,
        limite,
    )


def buscar_servico_service(
    db: Session,
    servico_id: int,
    empresa_id: int,
):
    return buscar_servico_por_id(db, servico_id, empresa_id)


def atualizar_servico_service(
    db: Session,
    servico_id: int,
    dados,
    empresa_id: int,
):
    servico_db = buscar_servico_por_id(db, servico_id, empresa_id)
    if not servico_db:
        raise HTTPException(
            status_code=404,
            detail="Servico nao encontrado.",
        )

    if hasattr(dados, "model_dump"):
        dados_dict = dados.model_dump(exclude_unset=True)
    else:
        dados_dict = dict(dados)

    if "nome" in dados_dict:
        dados_dict["nome"] = _validar_nome(dados_dict["nome"])

    if "preco_padrao" in dados_dict:
        _validar_preco(dados_dict["preco_padrao"])
    if "categoria" in dados_dict:
        dados_dict["categoria"] = _normalizar_categoria(dados_dict["categoria"])

    if "tipo_recurso" in dados_dict:
        dados_dict["tipo_recurso"] = _normalizar_tipo_recurso(
            dados_dict["tipo_recurso"]
        )
    if "modo_selecao_recurso" in dados_dict:
        dados_dict["modo_selecao_recurso"] = ModoReservaRecurso(
            dados_dict["modo_selecao_recurso"]
        ).value

    requer_recurso = dados_dict.get(
        "requer_recurso", servico_db.requer_recurso
    )
    tipo_recurso = dados_dict.get("tipo_recurso", servico_db.tipo_recurso)
    if requer_recurso and not tipo_recurso:
        raise HTTPException(
            status_code=400,
            detail="O tipo_recurso e obrigatorio quando o servico exige recurso.",
        )
    modo_selecao = dados_dict.get(
        "modo_selecao_recurso", servico_db.modo_selecao_recurso
    )
    if requer_recurso and not modo_selecao:
        raise HTTPException(
            status_code=400,
            detail="O modo de selecao do recurso e obrigatorio.",
        )

    try:
        servico_atualizado = atualizar_servico(
            db,
            servico_db,
            dados_dict,
        )
        db.commit()
        db.refresh(servico_atualizado)
        return servico_atualizado
    except Exception:
        db.rollback()
        raise


def deletar_servico_service(
    db: Session,
    servico_id: int,
    empresa_id: int,
):
    servico_db = buscar_servico_por_id(db, servico_id, empresa_id)
    if not servico_db:
        raise HTTPException(
            status_code=404,
            detail="Servico nao encontrado.",
        )

    try:
        servico_desativado = desativar_servico(db, servico_db)
        db.commit()
        db.refresh(servico_desativado)
        return servico_desativado
    except Exception:
        db.rollback()
        raise
