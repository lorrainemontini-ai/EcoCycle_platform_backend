"""Validação de entrada de producao; campos originais preservados."""

from pydantic import BaseModel


class ProducaoCreate(BaseModel):

    turno: str  # Ex: manhã, tarde, noite
    material_processado: str # Ex: "plástico PET"
    quantidade_entrada_kg: float # peso bruto que entrou na linha de produção
    quantidade_saida_kg: float   # Peso limpo/enfardado gerado após separação
    refugo_kg: float # material descartado/impróprio
