"""Validação de entrada de fornecedores; campos originais preservados."""

from pydantic import BaseModel


class FornecedoresCreate(BaseModel):
    nome: str
    cnpj: str
    contato: str

