"""Ponto de entrada da API; executado com uvicorn main:app."""

from fastapi import FastAPI

from routers import api_router

# Uma única aplicação substitui as seis inicializações repetidas do arquivo original.
app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente.",
)

# O registro centralizado inclui as rotas de negócio e o diagnóstico do banco.
app.include_router(api_router)


@app.get("/", tags=["Início"])
def home():
    """Preserva a resposta original de disponibilidade do backend."""
    return {"mensagem": "API está online e operacional!"}
