from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api", tags=["alertas"])

# modelo de integridade
class AlertasUpdate(BaseModel):
    id_alerta: str
    id_leitura: str
    id_esteira: str
    nome_esteira: str
    status_esteira: str
    temperatura_esteira_c: float # temperatura_esteira_c do motor em ºC
    velocidade_esteira_kmh: float
    peso_atual_kg: float # carga de peso da esteira
    travada: bool # True se houver travamento mecânico
    datahora_alerta: datetime
    concluido: bool

# integração com o banco de dados
alertas_db = {
    "id_esteira": 1,
    "nome_esteira": "Esteira Principal de Separação",
    "status_esteira": "LIGADA",
    "temperatura_esteira_c": 38.5,
    "velocidade_esteira_kmh": 4.0,
    "peso_esteira_kg": 120.0,
    "travada": False,
    "concluido": False
}

# consultar alertas
@router.get("/alertas")
def listar_alertas():
    return {"lalertas": alertas_db}

# atualizar status da esteira
@router.post("/alertas", status_code=status.HTTP_200_OK)
def atualizar_dados_esteira(dados: AlertasUpdate):

    # ponte com o middleware em php, recebe as leituras do sensor físico para avaliação dentro da api
    alertas_gerados = []
    status_calculado = "LIGADA"

    if dados.peso_atual_kg > 500.0: # regra de sobrepeso
        alertas_gerados.append("ALERTA! SOBRECARGA DE PESO DETECTADA")

    if dados.temperatura_esteira_c > 50.0: # regra de superaquecimento
        alertas_gerados.append("ALERTA! SUPERAQUECIMENTO DO MOTOR")

    if dados.velocidade_esteira_kmh > 10.0: # regra de velocidade
            alertas_gerados.append("ALERTA! ESTEIRA ACIMA DA VELOCIDADE")

    if dados.velocidade_esteira_kmh > 1.0: # regra de velocidade
            alertas_gerados.append("ALERTA! ESTEIRA ABAIXO DA VELOCIDADE")

    if  dados.travada: # trava por dejeto
        alertas_gerados.append("ALERTA! ESTEIRA TRAVADA POR SEGURANÇA")

    # problemas graves alteram o status da esteira
    if len(alertas_gerados) > 0:
        status_calculado = "ESTEIRA DESLIGADA"
    else:
        status_calculado = "LIGADA"

    alertas_db["status_esteira"] = status_calculado
    alertas_db["temperatura_esteira_c"] = dados.temperatura_esteira_c
    alertas_db["velocidade_esteira_kmh"] = dados.velocidade_esteira_kmh
    alertas_db["peso_atual_kg"] = dados.peso_atual_kg
    alertas_db["travada"] = dados.travada

    return {
        "mensagem": "Dados do middleware processados com sucesso",
        "estado_atual": alertas_db,
        "alertas_seguranca": alertas_gerados,
        "acao_tomada": (
            "Sistema operando ormalmente"
            if len(alertas_gerados) == 0
            else "DESLIGAMENTOS DE SEGURANÇA ACIONADO"
        )
    }