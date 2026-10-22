"""Validação de entrada de auth; campos originais preservados."""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    usuario: str
    senha: str
