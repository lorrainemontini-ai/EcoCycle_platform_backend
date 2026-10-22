from fastapi import APIRouter, status
from pydantic import BaseModel, Field

#cria o  roteador de lotes
router = APIRouter(prefix= "/api", tags=["Lotes"])

# modelo de integridade de dados
class LoteCreate(BaseModel):
    id_fornecedor: int = Field(description="ID do fornecedor que entregou o lote.", examples=[1])
    tipo_material: str = Field(description="Tipo de material do lote.", examples=["Plástico PET"])
    peso_inicial_kg: float = Field(description="Peso inicial do lote, em quilogramas.", examples=[450.5])
    observacao: str = Field(description="Observações sobre o lote.", examples=["Lote limpo entregue pela cooperativa parceira."])

# integração com banco de dados
lotes_db = [
    {
        "id_lote": 1,
        "id_fornecedor": 1,
        "tipo-material": "Plástico PET",
        "peso_inicial_kg": 450.5,
        "observacao": "Lote limpo entregue pela cooperativa parceira." 
    }
]

# consultar lotes cadastrados
@router.get(
    "/lotes",
    summary="Listar lotes",
    description="Retorna todos os lotes de material recebidos dos fornecedores.",
    response_description="Lista de lotes cadastrados.",
)
def listar_lotes():
    return {"lotes": lotes_db}

# cadastrar lotes
@router.post(
    "/lotes",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar lote",
    description="Registra um novo lote recebido. O `id_lote` é gerado automaticamente de forma sequencial.",
    response_description="Lote registrado com sucesso.",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Lote  registrado com sucesso!",
                        "lote": {
                            "id_lote": 2,
                            "id_fornecedor": 1,
                            "tipo_material": "Plástico PET",
                            "peso_inicial_kg": 450.5,
                            "observacao": "Lote limpo entregue pela cooperativa parceira."
                        }
                    }
                }
            }
        },
        422: {"description": "Erro de validação: campo obrigatório ausente ou com tipo inválido."},
    },
)
def cadastrar_lote(lote: LoteCreate):

    novo_lote = {
        "id_lote": len(lotes_db) + 1,
        "id_fornecedor": lote.id_fornecedor,
        "tipo_material": lote.tipo_material,
        "peso_inicial_kg": lote.peso_inicial_kg,
        "observacao": lote.observacao
    }

    lotes_db.append(novo_lote)

    return {
        "mensagem": "Lote  registrado com sucesso!",
        "lote": novo_lote
    }
