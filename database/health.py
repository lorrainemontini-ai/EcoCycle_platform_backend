"""Diagnóstico de leitura sobre uma tabela explicitamente configurada."""

import os
import re

from database.supabase_client import SupabaseConfigurationError, get_supabase_client


def check_database() -> None:
    """Verifica a API de dados sem escrever nem retornar registros."""
    # A criação do cliente carrega o .env antes da leitura das opções de diagnóstico.
    client = get_supabase_client()
    table = os.environ.get("SUPABASE_HEALTH_TABLE", "").strip()
    column = os.environ.get("SUPABASE_HEALTH_COLUMN", "").strip()
    # Os identificadores vêm do servidor, nunca de parâmetros públicos da rota.
    if not all(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", value) for value in (table, column)):
        raise SupabaseConfigurationError("Configure a tabela e a coluna de diagnóstico.")
    # HEAD consulta uma relação real, inclusive vazia, sem transferir seu conteúdo.
    client.table(table).select(column, head=True).limit(1).execute()