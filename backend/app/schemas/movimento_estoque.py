from pydantic import BaseModel, StrictInt, model_validator
from datetime import datetime


class ProdutoResumo(BaseModel):

    id: int
    nome: str

    class Config:
        from_attributes = True



class MovimentoEstoqueCreate(BaseModel):

    produto_id: int

    tipo: str

    quantidade: StrictInt

    observacao: str | None = None


    @model_validator(mode="after")
    def validar_quantidade_por_tipo(self):

        tipo = self.tipo.upper()

        if tipo == "AJUSTE" and self.quantidade < 0:

            raise ValueError(
                "Saldo de ajuste n\u00e3o pode ser negativo."
            )

        if tipo != "AJUSTE" and self.quantidade <= 0:

            raise ValueError(
                "Quantidade deve ser maior que zero."
            )

        return self





class MovimentoEstoqueResponse(BaseModel):

    id: int

    empresa_id: int

    produto_id: int

    usuario_id: int

    tipo: str

    quantidade: StrictInt

    estoque_anterior: StrictInt | None = None

    estoque_posterior: StrictInt | None = None

    observacao: str | None = None

    created_at: datetime

    produto: ProdutoResumo | None = None



    class Config:

        from_attributes = True
