"""Registro central dos roteadores da aplicação."""

from fastapi import APIRouter

from routers import auth, equipamentos, fornecedores, lotes, materiais, producao, health

# Cada módulo mantém seu prefixo e seus contratos originais.
api_router = APIRouter()
for router in (
    auth.router, fornecedores.router, materiais.router, lotes.router,
    equipamentos.router, producao.router, health.router,
):
    api_router.include_router(router)
