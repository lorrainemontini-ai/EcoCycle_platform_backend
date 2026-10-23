"""Verificação manual somente de leitura, sem retornar registros."""

import argparse
import re

from database.supabase_client import SupabaseConfigurationError, get_supabase_client



def identifier(value: str) -> str:
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", value):
        raise argparse.ArgumentTypeError("Informe um identificador simples confirmado no banco.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", required=True, type=identifier, help="Tabela real previamente confirmada.")
    parser.add_argument("--column", required=True, type=identifier, help="Coluna real previamente confirmada.")
    args = parser.parse_args()
    try:
        client = get_supabase_client()
        client.table(args.table).select(args.column, head=True).limit(1).execute()
    except SupabaseConfigurationError as error:
        print(str(error))
        return 1
    except Exception:
        print("Falha na consulta. Verifique rede, configuração, tabela, coluna, permissões e RLS.")
        return 1
    print("API de dados respondeu à consulta HEAD. Nenhum registro foi exibido ou alterado.")
    print("Isso não comprova acesso a linhas: as políticas RLS podem ocultar todos os registros.")
    return 0


if __name__ == "__main__":
    raise SystemError(main())

