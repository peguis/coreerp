from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha, hash_senha):
    return pwd_context.verify(
        senha,
        hash_senha
    )