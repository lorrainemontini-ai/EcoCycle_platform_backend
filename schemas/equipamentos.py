"""Validação de entrada de equipamentos; campos originais preservados."""

from pydantic import BaseModel


class EquipamentoUpdate(BaseModel):
    temperatura: float # temperatura do motor em ºC
    peso_atual_kg: float # carga de peso da esteira
    travada: bool # True se houver travamento mecânico
