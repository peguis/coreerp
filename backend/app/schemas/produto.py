from typing import Optional

from pydantic import BaseModel


class ProdutoCreate(BaseModel):

    nome: str
    categoria: Optional[str] = None
    codigo_interno: Optional[str] = None
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    unidade: Optional[str] = "UN"
    descricao: Optional[str] = None
    estoque_minimo: int = 0
    estoque_maximo: int = 0

    preco: float
    estoque: int


class ProdutoResponse(BaseModel):

    id: int
    empresa_id: int

    nome: str
    categoria: Optional[str]
    codigo_interno: Optional[str]
    codigo_barras: Optional[str]
    marca: Optional[str]
    unidade: Optional[str]
    descricao: Optional[str]
    estoque_minimo: int
    estoque_maximo: int

    preco: float
    estoque: int
    ativo: bool

    class Config:
        from_attributes = True