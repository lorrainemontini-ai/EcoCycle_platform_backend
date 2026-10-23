"""Cliente compartilhado sem sessão de usuário e sujeito às políticas RLS."""

import os
from pathlib import Path
from threading import Lock
from urllib.parse import urlsplit

from dotenv import load_dotenv
from supabase import Client, ClientOptions, create_client

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
# O bloqueio impede a criação duplicada do cliente em requisições simultâneas.
_client: Client | None = None
_client_lock = Lock()


class SupabaseConfigurationError(RuntimeError):
    """Indica configuração inválida sem expor valores sensíveis."""


def _read_settings() -> tuple[str, str]:
    try:
        load_dotenv(dotenv_path=ENV_FILE, override=False)
    except (OSError, UnicodeError):
        raise SupabaseConfigurationError("Não foi possível carregar o arquivo .env.") from None

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        raise SupabaseConfigurationError("Configure SUPABASE_URL e SUPABASE_KEY no ambiente ou no .env.")

    try:
        parsed = urlsplit(url)
        valid_url = (
            parsed.scheme == "https" and parsed.hostname and parsed.port in (None, 443)
            and not parsed.username and not parsed.password
            and parsed.path in ("", "/") and not parsed.query and not parsed.fragment
        )
    except ValueError:
        valid_url = False
    if not valid_url:
        raise SupabaseConfigurationError("SUPABASE_URL deve ser a URL HTTPS do projeto, sem credenciais ou caminhos.")
    if not key.startswith("sb_publishable_") or len(key) <= len("sb_publishable_") or any(c.isspace() for c in key):
        raise SupabaseConfigurationError("SUPABASE_KEY deve ser uma chave publicável (sb_publishable_). Chaves administrativas e legadas não são aceitas.")
    return url.rstrip("/"), key


def get_supabase_client() -> Client:
    """Cria uma vez por processo, somente quando solicitado; não consulta tabelas.

    Não autentique usuários nem altere cabeçalhos neste cliente compartilhado.
    A autenticação futura exigirá contexto isolado por requisição.
    """
    global _client
    with _client_lock:
        if _client is None:
            url, key = _read_settings()
            try:
                _client = create_client(
                    url, key,
                    # Limita a espera pela API de dados e mantém o cliente sem sessão.
                    options=ClientOptions(
                        persist_session=False, auto_refresh_token=False,
                        postgrest_client_timeout=5,
                    ),
                )
            except Exception:
                raise SupabaseConfigurationError("Não foi possível inicializar o cliente Supabase. Verifique a configuração.") from None
        return _client
