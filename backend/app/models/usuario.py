from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True
    )

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False,
        index=True
    )

    empresa = relationship(
        "Empresa",
        back_populates="usuarios"
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

    senha = Column(
        String,
        nullable=False
    )

    ativo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    nullable=False
    )