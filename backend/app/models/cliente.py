from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Cliente(Base):

    __tablename__ = "clientes"

    id = Column(
        Integer,
        primary_key=True
    )

    nome = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    telefone = Column(
        String,
        nullable=True
    )

    ativo = Column(
        Boolean,
        default=True
    )