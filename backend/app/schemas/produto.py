from typing import Optional

from pydantic import BaseModel
from typing import Optional, List


class ProdutoCreate(BaseModel):

    nome: str

    categoria: Optional[str] = None
    codigo_interno: Optional[str] = None
    codigo_barras: Optional[str] = None
    marca: Optional[str] = None
    unidade: Optional[str] = "UN"
    descricao: Optional[str] = None

    preco: float
    estoque: float = 0

    estoque_minimo: float = 0
    estoque_maximo: float = 0

    peso: Optional[float] = None
    altura: Optional[float] = None
    largura: Optional[float] = None
    comprimento: Optional[float] = None

    localizacao: Optional[str] = None

    custo_medio: float = 0

class ProdutoImagemResponse(BaseModel):

    id: int
    nome_arquivo: str
    caminho: str
    principal: bool

    class Config:
        from_attributes = True


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

    preco: float
    estoque: float

    estoque_minimo: float
    estoque_maximo: float

    peso: Optional[float]
    altura: Optional[float]
    largura: Optional[float]
    comprimento: Optional[float]

    localizacao: Optional[str]

    custo_medio: float

    ativo: bool

    imagens: List[ProdutoImagemResponse] = []

    class Config:
        from_attributes = True