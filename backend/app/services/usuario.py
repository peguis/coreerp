from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioCreate

from app.repositories.usuario import (
    criar_usuario,
    listar_usuarios,
    buscar_usuario_por_id,
    atualizar_usuario,
    deletar_usuario,
    buscar_por_email
)

from app.auth.hash import verificar_senha
from app.auth.jwt import criar_token

from app.core.validators.usuario import validar_usuario
from app.core.enums import PerfilUsuario
from app.models.empresa import Empresa



def criar_usuario_service(
    db: Session,
    usuario: UsuarioCreate,
    empresa_id: int
):

    validar_usuario(usuario)

    if usuario.perfil == PerfilUsuario.VENDEDOR_PEGS:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if not empresa or not empresa.eh_matriz:
            raise HTTPException(status_code=400, detail="Vendedor Pegs só pode pertencer à Matriz Pegs.")
    criado = criar_usuario(
        db,
        usuario,
        empresa_id
    )
    if usuario.perfil == PerfilUsuario.PEGS_ADMIN:
        empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
        if empresa and not empresa.eh_matriz:
            empresa.eh_matriz = True
            db.commit()
            db.refresh(criado)
    return criado





def listar_usuarios_service(
    db: Session,
    empresa_id: int
):

    return listar_usuarios(
        db,
        empresa_id
    )





def buscar_usuario_service(
    db: Session,
    usuario_id: int,
    empresa_id: int
):

    return buscar_usuario_por_id(
        db,
        usuario_id,
        empresa_id
    )





def atualizar_usuario_service(
    db: Session,
    usuario_id: int,
    empresa_id: int,
    dados
):

    usuario = buscar_usuario_por_id(
        db,
        usuario_id,
        empresa_id
    )


    if not usuario:
        return None



    if hasattr(dados, "model_dump"):
        dados_dict = dados.model_dump(exclude_unset=True)
    else:
        dados_dict = dict(dados)


    if "nome" in dados_dict:

        if len(
            dados_dict["nome"].strip()
        ) < 3:

            return None



    if "senha" in dados_dict:

        if len(
            dados_dict["senha"]
        ) < 6:

            return None


    if "perfil" in dados_dict:

        perfil = dados_dict["perfil"]

        if hasattr(perfil, "value"):

            dados_dict["perfil"] = perfil.value

        if dados_dict["perfil"] == PerfilUsuario.VENDEDOR_PEGS.value:
            empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
            if not empresa or not empresa.eh_matriz:
                raise HTTPException(status_code=400, detail="Vendedor Pegs só pode pertencer à Matriz Pegs.")



    return atualizar_usuario(
        db,
        usuario,
        dados_dict
    )





def deletar_usuario_service(
    db: Session,
    usuario_id: int,
    empresa_id: int
):

    usuario = buscar_usuario_por_id(
        db,
        usuario_id,
        empresa_id
    )


    if not usuario:

        return False



    deletar_usuario(
        db,
        usuario
    )


    return True





def login_service(
    db,
    dados
):

    usuario = buscar_por_email(
        db,
        dados.username
    )


    if not usuario:

        return None


    if not usuario.ativo or not usuario.empresa.ativo:

        return None



    if not verificar_senha(
        dados.password,
        usuario.senha
    ):

        return None



    token = criar_token(
        {
            "sub": usuario.email,
            "empresa_id": usuario.empresa_id,
            "perfil": usuario.perfil
        }
    )


    return {

        "access_token": token,

        "token_type": "bearer"

    }
