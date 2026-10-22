from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

# cria o roteador focado nas operações internas e no dashboard
router = APIRouter (prefix="/api", tags=["Produção e Dashboard"])

# modelo de integridade de dados
class ProducaoCreate(BaseModel):
    id_producao: str
    id_lote: str
    turno: str  # Ex: manhã, tarde, noite
    id_usuario: str
    id_esteira: str
    id_material: str # Ex: "plástico PET"
    quantidade_entrada_kg: float # peso bruto que entrou na linha de produção
    quantidade_saida_kg: float   # Peso limpo/enfardado gerado após separação
    rejeito_kg: float # material descartado/impróprio
    status_producao: str
    data_inicio: datetime
    date_fim: datetime

# integração com o banco de dados
producao_db = [
    {
        "id_producao": 1,
        "id_lote": 7563,
        "turno": "Manhã",
        "id_usuario": 15,
        "id_esteira": 1250,
        "id_material": "Plástico PET",
        "quantidade_entrada_kg": 450.0,
        "quantidade_saida_kg": 100.0,
        "rejeito_kg": 10.0,
        "status_producao":str,
        "data_inicio": 10/10/2026,
        "data_fim": 17/10/2026
    }
]

# consultar todos os registros da produção
@router.get("//producao")
def listar_producao():
    return {"registros_producao": producao_db}

# registrar nova producao
@router.post("/producao", status_code=status.HTTP_201_CREATED)
def registrar_producao(producao: ProducaoCreate):
    nova_producao = {
        "id_producao": len(producao_db) + 1,
        "id_lote": producao.id_lote,
        "turno": producao.turno,
        "id_usuario": producao.id_usuario,
        "id_esteira": producao.id_esteira,
        "id_material": producao.id_material,
        "quantidade_entrada_kg": producao.quantidade_entrada_kg,
        "quantidade_saida_kg": producao.quantidade_saida_kg,
        "rejeito_kg": producao.rejeito_kg,
        "status_producao": producao.status_producao,
        "data_inicio": 18/10/2026,
        "data_fim": 21/10/2026
    }

    producao_db.append(nova_producao)

    return {
        "mensagem": "Ciclo de produção registrado com sucesso!",
        "producao": nova_producao
    }

# relatório de toda produção e produto que da entrada e saída
@router.get("/producao/dashboard-diario")
def Dashboard_diario():
    total_entrada = sum(item["quantidade_entrada_kg"] for item in producao_db)
    total_saida = sum(item["quantidade_saida_kg"] for item in producao_db)
    total_rejeito = sum(item["rejeito_kg"] for item in producao_db)

    # calculo da reciclagem
    percentual = (total_saida / total_entrada * 100) if total_entrada > 0 else 0.0

    return {
        "indicador": "Dashboard Consolidado Diário - EcoCycle",
        "total_turnos_registrados": len(producao_db),
        "balanco_massas_kg": {
            "total_material_entrada": total_entrada,
            "total_produzido_saida": total_saida,
            "total_rejeitos_perdas": total_rejeito
        },
        "indicadores_desempenho": {
            "aproveitamento_percentual": round(percentual, 2)
        },
        "detalhado_por_turno": producao_db
    }