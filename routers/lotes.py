from fastapi import APIRouter, status
# Modelo movido para schemas; importação preserva o acesso pelo módulo original.
from schemas.lotes import LoteCreate

#cria o  roteador de lotes
router = APIRouter(prefix= "/api", tags=["Lotes"])

# Armazenamento simulado em memória; ainda não persiste no Supabase.
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
@router.get("/lotes")
def listar_lotes():
    return {"lotes": lotes_db}

# cadastrar lotes
@router.post("/lotes", status_code=status.HTTP_201_CREATED)
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
