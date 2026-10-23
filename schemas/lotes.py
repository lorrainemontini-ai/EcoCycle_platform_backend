"""Validação de entrada de lotes; campos originais preservados."""

from pydantic import BaseModel


class LoteCreate(BaseModel):
    id_fornecedor: int
    tipo_material: str
    peso_inicial_kg: float
    observacao: str
