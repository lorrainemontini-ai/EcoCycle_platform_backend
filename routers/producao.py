from fastapi import APIRouter, status
from pydantic import BaseModel, Field

# cria o roteador focado nas operações internas e no dashboard
router = APIRouter (prefix="/api", tags=["Produção e Dashboard"])

# modelo de integridade de dados
class ProducaoCreate(BaseModel):

    turno: str = Field(description="Turno de trabalho (manhã, tarde, noite).", examples=["Manhã"])  # Ex: manhã, tarde, noite
    material_processado: str = Field(description="Material processado no turno.", examples=["Plástico PET"]) # Ex: "plástico PET"
    quantidade_entrada_kg: float = Field(description="Peso bruto que entrou na linha de produção, em kg.", examples=[450.0]) # peso bruto que entrou na linha de produção
    quantidade_saida_kg: float = Field(description="Peso limpo/enfardado gerado após a separação, em kg.", examples=[100.0])   # Peso limpo/enfardado gerado após separação
    refugo_kg: float = Field(description="Material descartado/impróprio, em kg.", examples=[10.0]) # material descartado/impróprio

# integração com o banco de dados
producao_db = [
    {
        "id_producao": 1,
        "turno": "Manhã",
        "material_processados": "Plástico PET",
        "quantidade_entrada_kg": 450.0,
        "quantidade_saida_kg": 100.0,
        "refugo_kg": 10.0
    }
]

# consultar todos os registros da produção
@router.get(
    "//producao",
    summary="Listar registros de produção",
    description="Retorna todos os ciclos de produção registrados (turno, material, entrada, saída e refugo).",
    response_description="Lista de registros de produção.",
)
def listar_producao():
    return {"registros_producao": producao_db}

# registrar nova producao
@router.post(
    "/producao",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar ciclo de produção",
    description="Registra um novo ciclo de produção de um turno. O `id_producao` é gerado automaticamente de forma sequencial.",
    response_description="Ciclo de produção registrado com sucesso.",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Ciclo de produção registrado com sucesso!",
                        "producao": {
                            "id_producao": 2,
                            "turno": "Tarde",
                            "material_processado": "Plástico PET",
                            "quantidade_entrada_kg": 450.0,
                            "quantidade_saida_kg": 380.0,
                            "refugo_kg": 10.0
                        }
                    }
                }
            }
        },
        422: {"description": "Erro de validação: campo obrigatório ausente ou com tipo inválido."},
    },
)
def registrar_producao(producao: ProducaoCreate):
    nova_producao = {
        "id_producao": len(producao_db) + 1,
        "turno": producao.turno,
        "material_processado": producao.material_processado,
        "quantidade_entrada_kg": producao.quantidade_entrada_kg,
        "quantidade_saida_kg": producao.quantidade_saida_kg,
        "refugo_kg": producao.refugo_kg
    }

    producao_db.append(nova_producao)

    return {
        "mensagem": "Ciclo de produção registrado com sucesso!",
        "producao": nova_producao
    }

# relatório de toda produção e produto que da entrada e saída
@router.get(
    "/producao/dashboard-diario",
    summary="Dashboard diário de produção",
    description=(
        "Consolida todos os registros de produção: balanço de massas (entrada, saída e rejeitos) "
        "e o aproveitamento percentual, calculado como `saída / entrada × 100` "
        "(0.0 quando não há entrada)."
    ),
    response_description="Dashboard consolidado com balanço de massas e indicadores.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "indicador": "Dashboard Consolidado Diário - EcoCycle",
                        "total_turnos_registrados": 1,
                        "balanco_massas_kg": {
                            "total_material_entrada": 450.0,
                            "total_produzido_saida": 100.0,
                            "total_rejeitos_perdas": 10.0
                        },
                        "indicadores_desempenho": {"aproveitamento_percentual": 22.22},
                        "detalhado_por_turno": []
                    }
                }
            }
        }
    },
)
def Dashboard_diario():
    total_entrada = sum(item["quantidade_entrada_kg"] for item in producao_db)
    total_saida = sum(item["quantidade_saida_kg"] for item in producao_db)
    total_refugo = sum(item["refugo_kg"] for item in producao_db)

    # calculo da reciclagem
    percentual = (total_saida / total_entrada * 100) if total_entrada > 0 else 0.0

    return {
        "indicador": "Dashboard Consolidado Diário - EcoCycle",
        "total_turnos_registrados": len(producao_db),
        "balanco_massas_kg": {
            "total_material_entrada": total_entrada,
            "total_produzido_saida": total_saida,
            "total_rejeitos_perdas": total_refugo
        },
        "indicadores_desempenho": {
            "aproveitamento_percentual": round(percentual, 2)
        },
        "detalhado_por_turno": producao_db
    }
