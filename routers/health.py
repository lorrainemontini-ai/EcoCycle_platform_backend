"""Rota de diagnóstico do banco, separada das operações de negócio."""

from fastapi import APIRouter, HTTPException, Response, status

from database.health import check_database

router = APIRouter(prefix="/api", tags=["Diagnóstico"])


@router.get("/health/database", responses={503: {"description": "Banco indisponível ou diagnóstico não configurado."}})
def database_health(response: Response):
    """Testa uma leitura no Supabase sem expor registros ou configuração."""
    # Evita que o navegador apresente um diagnóstico antigo como resultado atual.
    response.headers["Cache-Control"] = "no-store"
    try:
        check_database()
    except Exception:
        # O diagnóstico público retorna estado genérico, sem erros do provedor.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Banco indisponível ou diagnóstico não configurado.",
            headers={"Cache-Control": "no-store"},
        )  from None
    return {"status": "ok", "mensagem": "Consulta de leitura ao banco concluída pela API do Supabase."}
