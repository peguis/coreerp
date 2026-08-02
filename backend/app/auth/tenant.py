from fastapi import Depends

from app.auth.dependencies import get_current_user



def get_empresa_id(
    usuario=Depends(get_current_user)
):

    return usuario.empresa_id





def get_usuario_id(
    usuario=Depends(get_current_user)
):

    return usuario.id





def get_usuario(
    usuario=Depends(get_current_user)
):

    return usuario