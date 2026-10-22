from fastapi import APIRouter, status
from pydantic import BaseModel

from .alertas import gerar_alertas

# cria o roteador focado nas esteiras e no chão da fábrica
router = APIRouter(prefix="/api", tags=["Equipamentos"])


# modelo de integridade
class EquipamentoUpdate(BaseModel):
    id_esteira: str
    nome_esteira: str
    status_esteira: str
    temperatura_esteira_c: float # temperatura_esteira_c do motor em ºC
    velocidade_esteira_kmh: float
    peso_atual_kg: float # carga de peso da esteira
    travada: bool # True se houver travamento mecânico

# integração com o banco de dados
equipamentos_db = {
    "id_esteira": 1,
    "nome_esteira": "Esteira Principal de Separação",
    "status_esteira": "LIGADA",
    "temperatura_esteira_c": 38.5,
    "velocidade_esteira_kmh": 4.0,
    "peso_esteira_kg": 120.0,
    "travada": False
}


# consultar status do equipamento e dados
@router.get("/equipamentos")
def consultar_equipamentos():
    return equipamentos_db


# atualizar status da esteira
@router.post("/equipamentos/status", status_code=status.HTTP_200_OK)
def atualizar_dados_esteira(dados: EquipamentoUpdate):
    # ponte com o middleware em php, recebe as leituras do sensor físico para avaliação dentro da api
    alertas_gerados = gerar_alertas(dados.temperatura, dados.peso_atual_kg, dados.travada)

    # problemas graves alteram o status da esteira
    status_calculado = "ESTEIRA DESLIGADA" if alertas_gerados else "LIGADA"

    equipamentos_db["status_esteira"] = status_calculado
    equipamentos_db["temperatura_esteira_c"] = dados.temperatura_esteira_c
    equipamentos_db["peso_atual_kg"] = dados.peso_atual_kg
    equipamentos_db["travada"] = dados.travada

    return {
        "mensagem": "Dados do middleware processados com sucesso",
        "estado_atual": equipamentos_db,
        "alertas_seguranca": alertas_gerados,
        "acao_tomada": (
            "Sistema operando normalmente"
            if not alertas_gerados
            else "DESLIGAMENTO DE SEGURANÇA ACIONADO"
        ),
    }
