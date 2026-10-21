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
    description="Núcleo de serviços e API REST para o sistema de reciclagem inteligente."
)

# ativa a rota de produção
app.include_router(auth.router)
app.include_router(fornecedores.router)
app.include_router(materiais.router)
app.include_router(lotes.router)
app.include_router(equipamentos.router)
app.include_router(producao.router)  

@app.get("/", tags=["Início"])
def home():
    return {"mensagem": "API está online e operacional!"}