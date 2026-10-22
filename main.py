from fastapi import FastAPI
from routers import auth, lotes  # Importa o arquivo auth.py

app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente."
)

# ativa a rota de autenticação
app.include_router(auth.router) 

@app.get("/", tags=["Início"])
def home():
    return {"mensagem": "API está online e operacional!"}


from fastapi import FastAPI
from routers import fornecedores  # Importa o arquivo fornecedores.py

app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente."
)

# ativa rota de fornecedores
app.include_router(auth.router)
app.include_router(fornecedores.router)

@app.get("/", tags=["Início"])
def home():
    return {"mensagem": "API está online e operacional!"}


from fastapi import FastAPI
from routers import fornecedores, materiais #importa o arquivo materiais.py

app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente."
)

# ativa a rota de materiais
app.include_router(auth.router)
app.include_router(fornecedores.router)
app.include_router(materiais.router)

@app.get("/", tags=["início"])
def home():
    return {"mensagem": "API está online e operacional!"}


from fastapi import FastAPI
from routers import fornecedores, materiais, lotes #importa o arquivo lotes.py

app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente."
)

# ativa a rota de lotes
app.include_router(auth.router)
app.include_router(fornecedores.router)
app.include_router(materiais.router)
app.include_router(lotes.router)

@app.get("/", tags=["início"])
def home():
    return {"mensagem": "API está online e operacional!"}


from fastapi import FastAPI
from routers import fornecedores, materiais, lotes, equipamentos #importa o arquivo equipamentoss.py

app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente."
)

# ativa a rota de lotes
app.include_router(auth.router)
app.include_router(fornecedores.router)
app.include_router(materiais.router)
app.include_router(lotes.router)
app.include_router(equipamentos.router)

@app.get("/", tags=["início"])
def home():
    return {"mensagem": "API está online e operacional!"}


from fastapi import FastAPI
from routers import fornecedores, materiais, lotes, equipamentos, producao  # Importa o arquivo produção.py

app = FastAPI(
    title="EcoCycle API - Backend (Equipe 2)",
    version="1.0.0",
    description=(
        "Núcleo de serviços e API REST para o sistema de reciclagem inteligente.\n\n"
        "Módulos: autenticação, fornecedores, materiais, lotes, equipamentos (esteira) e "
        "produção/dashboard. Os dados são simulados em memória (sem banco de dados)."
    ),
    openapi_tags=[
        {"name": "Início", "description": "Verificação de disponibilidade da API."},
        {"name": "Autenticação e Segurança", "description": "Login e perfil de acesso (administrador ou operador)."},
        {"name": "Fornecedores", "description": "Cadastro e consulta de fornecedores de material."},
        {"name": "Materiais", "description": "Cadastro e consulta dos tipos de material (plástico, metal etc.)."},
        {"name": "Lotes", "description": "Registro e consulta dos lotes recebidos dos fornecedores."},
        {"name": "Equipamentos", "description": "Monitoramento da esteira e regras de segurança (peso, temperatura e travamento)."},
        {"name": "Produção e Dashboard", "description": "Registro de ciclos de produção e indicadores consolidados."},
    ]
)

# ativa a rota de produção
app.include_router(auth.router)
app.include_router(fornecedores.router)
app.include_router(materiais.router)
app.include_router(lotes.router)
app.include_router(equipamentos.router)
app.include_router(producao.router)  

@app.get(
    "/",
    tags=["Início"],
    summary="Status da API",
    description="Retorna uma mensagem confirmando que a API está online.",
)
def home():
    return {"mensagem": "API está online e operacional!"}