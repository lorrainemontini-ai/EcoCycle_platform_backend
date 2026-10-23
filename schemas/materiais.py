"""Validação de entrada de materiais; campos originais preservados."""

from pydantic import BaseModel


class  MaterialCreate(BaseModel):
    tipo: str # plástico ou metal
    classificacao: str # PET, PEAD, alumínio, ferro
    destino: str # esteira e setor
