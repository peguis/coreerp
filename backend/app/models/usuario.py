from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)

    nome = Column(String, nullable=False)

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
        DateTime,
        default=datetime.utcnow
    )

created_at = Column(
    DateTime,
    default=datetime.utcnow
)