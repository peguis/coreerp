from enum import Enum


class PerfilUsuario(str, Enum):
    ADMIN = "admin"
    GERENTE = "gerente"
    OPERADOR = "operador"
    CONSULTA = "consulta"