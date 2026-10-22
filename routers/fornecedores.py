from fastapi import  APIRouter, status
# Modelo movido para schemas; importação preserva o acesso pelo módulo original.
from schemas.fornecedores import FornecedoresCreate

# roteador para área de fornecedores
router = APIRouter(prefix="/api", tags=["Fornecedores"])

# Armazenamento simulado em memória; ainda não persiste no Supabase.
fornecedores_db = []

# consulta todos os fornecedores cadastrados
@router.get("/fornecedores")
def listar_fornecedores():

    return{"fornecedores": fornecedores_db}

# cadastrar novo fornecedor
@router.post("/fornecedores", status_code=status.HTTP_201_CREATED)
def cafastrar_fornecedores(fornecedor: FornecedoresCreate):

    novo_fornecedor = {
        "id_fornecedor": len(fornecedores_db) + 1, # adiciona +1 fornecedor a lista simulada
        "nome": fornecedor.nome,
        "cnpj": fornecedor.cnpj,
        "contato": fornecedor.contato
    }

    fornecedores_db.append(novo_fornecedor) # realiza a contagem da simulação

    return {
        "mensagem": "Fornecedor cadastrado com sucesso!",
        "fornecedor": novo_fornecedor
    }
