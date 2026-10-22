from fastapi import  APIRouter, status
from pydantic import BaseModel, Field

# roteador para área de fornecedores
router = APIRouter(prefix="/api", tags=["Fornecedores"])

# modelo de dados (Pydantic) para garantir integridade dos dados
class FornecedoresCreate(BaseModel):
    nome: str = Field(description="Nome ou razão social do fornecedor.", examples=["Cooperativa Verde Vida"])
    cnpj: str = Field(description="CNPJ do fornecedor.", examples=["12.345.678/0001-90"])
    contato: str = Field(description="Contato do fornecedor (telefone ou e-mail).", examples=["contato@verdevida.com.br"])

# integração com banco de dados
fornecedores_db = []

# consulta todos os fornecedores cadastrados
@router.get(
    "/fornecedores",
    summary="Listar fornecedores",
    description="Retorna todos os fornecedores cadastrados. A lista fica vazia até o primeiro cadastro.",
    response_description="Lista de fornecedores cadastrados.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "fornecedores": [
                            {
                                "id_fornecedor": 1,
                                "nome": "Cooperativa Verde Vida",
                                "cnpj": "12.345.678/0001-90",
                                "contato": "contato@verdevida.com.br"
                            }
                        ]
                    }
                }
            }
        }
    },
)
def listar_fornecedores(): 

    return{"fornecedores": fornecedores_db}

# cadastrar novo fornecedor
@router.post(
    "/fornecedores",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar fornecedor",
    description="Cadastra um novo fornecedor. O `id_fornecedor` é gerado automaticamente de forma sequencial.",
    response_description="Fornecedor cadastrado com sucesso.",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Fornecedor cadastrado com sucesso!",
                        "fornecedor": {
                            "id_fornecedor": 1,
                            "nome": "Cooperativa Verde Vida",
                            "cnpj": "12.345.678/0001-90",
                            "contato": "contato@verdevida.com.br"
                        }
                    }
                }
            }
        },
        422: {"description": "Erro de validação: campo obrigatório ausente ou com tipo inválido."},
    },
)
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
