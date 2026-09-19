from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.modulo import EmpresaModulo, Modulo


def inicializar_modulos_empresa(db: Session, empresa_id: int) -> None:
    modulos = db.query(Modulo).all()
    if not modulos:
        return
    agora = datetime.now(timezone.utc)
    db.add_all(
        [
            EmpresaModulo(
                empresa_id=empresa_id,
                modulo_id=modulo.id,
                ativo=True,
                ativado_em=agora,
            )
            for modulo in modulos
        ]
    )
    db.commit()


def listar_modulos_empresa(db: Session, empresa_id: int):
    registros = (
        db.query(Modulo, EmpresaModulo)
        .outerjoin(
            EmpresaModulo,
            (EmpresaModulo.modulo_id == Modulo.id)
            & (EmpresaModulo.empresa_id == empresa_id),
        )
        .order_by(Modulo.ordem, Modulo.nome)
        .all()
    )
    return [
        {
            "codigo": modulo.codigo,
            "nome": modulo.nome,
            "descricao": modulo.descricao,
            "obrigatorio": modulo.obrigatorio,
            "ordem": modulo.ordem,
            "ativo": bool(vinculo and vinculo.ativo),
            "ativado_em": vinculo.ativado_em if vinculo else None,
            "desativado_em": vinculo.desativado_em if vinculo else None,
        }
        for modulo, vinculo in registros
    ]


def atualizar_modulo_empresa(
    db: Session,
    empresa_id: int,
    codigo: str,
    ativo: bool,
):
    modulo = db.query(Modulo).filter(Modulo.codigo == codigo).first()
    if not modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado.")
    if modulo.obrigatorio and not ativo:
        raise HTTPException(
            status_code=400,
            detail="Módulos obrigatórios não podem ser desativados.",
        )

    vinculo = (
        db.query(EmpresaModulo)
        .filter(
            EmpresaModulo.empresa_id == empresa_id,
            EmpresaModulo.modulo_id == modulo.id,
        )
        .first()
    )
    agora = datetime.now(timezone.utc)
    if not vinculo:
        vinculo = EmpresaModulo(
            empresa_id=empresa_id,
            modulo_id=modulo.id,
            ativo=ativo,
            ativado_em=agora if ativo else None,
            desativado_em=None if ativo else agora,
        )
        db.add(vinculo)
    else:
        vinculo.ativo = ativo
        vinculo.ativado_em = agora if ativo else vinculo.ativado_em
        vinculo.desativado_em = None if ativo else agora

    db.commit()
    db.refresh(vinculo)
    return {
        "codigo": modulo.codigo,
        "nome": modulo.nome,
        "descricao": modulo.descricao,
        "obrigatorio": modulo.obrigatorio,
        "ordem": modulo.ordem,
        "ativo": vinculo.ativo,
        "ativado_em": vinculo.ativado_em,
        "desativado_em": vinculo.desativado_em,
    }
