from fastapi import APIRouter, status
# Modelo movido para schemas; importação preserva o acesso pelo módulo original.
from schemas.equipamentos import EquipamentoUpdate

# cria o roteador focado nas esteiras e no chão da fábrica
router = APIRouter (prefix="/api", tags=["Equipamentos"])

# Armazenamento simulado em memória; ainda não persiste no Supabase.
equipamentos_db = {
    "id_esteira": 1,
    "nome": "Esteira Principal de Separação",
    "status_operacional": "LIGADA",
    "temperatura": 38.5,
    "peso_atual_kh": 120.0,
    "travada": False
}

# consultar status do equipamentos e dados
@router.get("/equipamentos")
def consultar_equipamentos():

    return equipamentos_db

# atualizar status da esteira
@router.post("/equipamentos/status", status_code=status.HTTP_200_OK)
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
