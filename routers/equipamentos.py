from fastapi import APIRouter, status
from pydantic import BaseModel, Field

# cria o roteador focado nas esteiras e no chão da fábrica
router = APIRouter (prefix="/api", tags=["Equipamentos"])

# modelo de integridade
class EquipamentoUpdate(BaseModel):
    temperatura: float = Field(description="Temperatura do motor, em ºC. Acima de 50.0 gera alerta de superaquecimento.", examples=[38.5]) # temperatura do motor em ºC
    peso_atual_kg: float = Field(description="Carga de peso da esteira, em kg. Acima de 500.0 gera alerta de sobrecarga.", examples=[120.0]) # carga de peso da esteira
    travada: bool = Field(description="`true` se houver travamento mecânico (gera alerta e desliga a esteira).", examples=[False]) # True se houver travamento mecânico

# integração com o banco de dados
equipamentos_db = {
    "id_esteira": 1,
    "nome": "Esteira Principal de Separação",
    "status_operacional": "LIGADA",
    "temperatura": 38.5,
    "peso_atual_kh": 120.0,
    "travada": False
}

# consultar status do equipamentos e dados
@router.get(
    "/equipamentos",
    summary="Consultar status da esteira",
    description="Retorna o estado atual da esteira: nome, status operacional, temperatura, peso atual e se está travada.",
    response_description="Estado atual do equipamento.",
)
def consultar_equipamentos():

    return equipamentos_db

# atualizar status da esteira
@router.post(
    "/equipamentos/status",
    status_code=status.HTTP_200_OK,
    summary="Atualizar leituras da esteira",
    description=(
        "Recebe as leituras do sensor físico (via middleware em PHP), avalia as regras de segurança "
        "e atualiza o estado da esteira.\n\n"
        "**Regras de segurança:**\n"
        "- `peso_atual_kg` > 500.0 → alerta de sobrecarga de peso\n"
        "- `temperatura` > 50.0 → alerta de superaquecimento do motor\n"
        "- `travada` = true → alerta de esteira travada por segurança\n\n"
        "Se houver qualquer alerta, o status da esteira passa a `ESTEIRA DESLIGADA`; "
        "caso contrário, permanece `LIGADA`."
    ),
    response_description="Leituras processadas, com alertas e ação tomada.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Dados do middleware processados com sucesso",
                        "estado_atual": {
                            "id_esteira": 1,
                            "nome": "Esteira Principal de Separação",
                            "status_operacional": "ESTEIRA DESLIGADA",
                            "temperatura": 55.0,
                            "peso_atual_kg": 120.0,
                            "travada": False
                        },
                        "alertas_seguranca": ["ALERTA! SUPERAQUECIMENTO DO MOTOR"],
                        "acao_tomada": "DESLIGAMENTOS DE SEGURANÇA ACIONADO"
                    }
                }
            }
        },
        422: {"description": "Erro de validação: campo obrigatório ausente ou com tipo inválido."},
    },
)
def atualizar_dados_esteira(dados: EquipamentoUpdate):

    # ponte com o middleware em php, recebe as leituras do sensor físico para avaliação dentro da api
    alertas_gerados = []
    status_calculado = "LIGADA"

    if dados.peso_atual_kg > 500.0: # regra de sobrepeso
        alertas_gerados.append("ALERTA! SOBRECARGA DE PESO DETECTADA")

    if dados.temperatura > 50.0: # regra de superaquecimento
        alertas_gerados.append("ALERTA! SUPERAQUECIMENTO DO MOTOR")

    if  dados.travada: # trava por dejeto
        alertas_gerados.append("ALERTA! ESTEIRA TRAVADA POR SEGURANÇA")

    # problemas graves alteram o status da esteira
    if len(alertas_gerados) > 0:
        status_calculado = "ESTEIRA DESLIGADA"
    else:
        status_calculado = "LIGADA"

    equipamentos_db["status_operacional"] = status_calculado
    equipamentos_db["temperatura"] = dados.temperatura
    equipamentos_db["peso_atual_kg"] = dados.peso_atual_kg
    equipamentos_db["travada"] = dados.travada

    return {
        "mensagem": "Dados do middleware processados com sucesso",
        "estado_atual": equipamentos_db,
        "alertas_seguranca": alertas_gerados,
        "acao_tomada": (
            "Sistema operando ormalmente"
            if len(alertas_gerados) == 0
            else "DESLIGAMENTOS DE SEGURANÇA ACIONADO"
        )
    }
