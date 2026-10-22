from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

#cria o  roteador de lotes
router = APIRouter(prefix= "/api", tags=["Lotes"])

# modelo de integridade de dados
class LoteCreate(BaseModel):
    id_lote: str
    id_fornecedor: int
    status_lote: str
    peso_recebido_kg: float
    data_entrada: datetime
    observacao: str

# integração com banco de dados
lotes_db = [
    {
        "id_lote": 1,
        "id_fornecedor": 1,
        "status_lote": "Aceito",
        "peso_recebido_kg": 450.5,
        "data_entrada": "22/10/2026",
        "observacao": "Lote limpo entregue pela cooperativa parceira." 
    }
]

# consultar lotes cadastrados
@router.get("/lotes")
def listar_lotes():
    return {"lotes": lotes_db}

# cadastrar lotes
@router.post("/lotes", status_code=status.HTTP_201_CREATED)
def cadastrar_lote(lote: LoteCreate):

    novo_lote = {
        "id_lote": len(lotes_db) + 1,
        "id_fornecedor": lote.id_fornecedor,
        "status_lote": lote.status_lote,
        "peso_recebido_kg": lote.peso_recebido_kg,
        "data_entrada": lote.data_entrada,
        "observacao": lote.observacao
    }

    lotes_db.append(novo_lote)

    return {
        "mensagem": "Lote  registrado com sucesso!",
        "lote": novo_lote
    }