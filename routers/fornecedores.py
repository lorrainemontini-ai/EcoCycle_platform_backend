from fastapi import  APIRouter, status
from pydantic import BaseModel

# roteador para área de fornecedores
router = APIRouter(prefix="/api", tags=["Fornecedores"])

# modelo de dados (Pydantic) para garantir integridade dos dados
class FornecedoresCreate(BaseModel):
    nome_fornecedor: str
    id_cnpj: str
    telefone_fornecedor: str
    email_fornecedor: str
    endereco_fornecedor: str

# integração com banco de dados
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
        "nome_fornecedor": fornecedor.nome_fornecedor,
        "cnpj": fornecedor.id_cnpj,
        "telefone_fornecedor": fornecedor.telefone_fornecedor,
        "email_fornecedor": fornecedor.email_fornecedor,
        "endereco": fornecedor.endereco_fornecedor
    }

    fornecedores_db.append(novo_fornecedor) # realiza a contagem da simulação

    return {
        "mensagem": "Fornecedor cadastrado com sucesso!",
        "fornecedor": novo_fornecedor
    }