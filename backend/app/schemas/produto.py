from typing import Optional, List

from datetime import datetime

from pydantic import BaseModel, Field





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

    categoria: Optional[str] = None

    codigo_interno: Optional[str] = None

    codigo_barras: Optional[str] = None

    marca: Optional[str] = None

    unidade: Optional[str] = None

    descricao: Optional[str] = None



    preco: float

    estoque: float



    estoque_minimo: float

    estoque_maximo: float



    peso: Optional[float] = None

    altura: Optional[float] = None

    largura: Optional[float] = None

    comprimento: Optional[float] = None



    localizacao: Optional[str] = None



    custo_medio: float



    ultima_entrada: Optional[datetime] = None

    ultima_saida: Optional[datetime] = None



    ativo: bool



    imagens: List[ProdutoImagemResponse] = Field(
        default_factory=list
    )



    class Config:

        from_attributes = True