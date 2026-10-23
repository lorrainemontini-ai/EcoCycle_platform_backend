"""Testes do diagnóstico: sucesso, indisponibilidade e ausência de escrita."""

import os
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient
from supabase import ClientOptions, create_client

from database import health
from database.supabase_client import SupabaseConfigurationError
from main import app


class DatabaseHealthTests(unittest.TestCase):
    def test_real_sdk_uses_only_head_without_credentials_in_response(self):
        # O SDK real usa transporte HTTP simulado; nenhuma conexão externa é feita.
        requests = []

        def handle(request):
            requests.append(request)
            return httpx.Response(200, headers={"content-range": "*/0"})

        with httpx.Client(transport=httpx.MockTransport(handle)) as transport:
            client = create_client(
                "https://example.supabase.co", "sb_publishable_teste",
                options=ClientOptions(httpx_client=transport, persist_session=False, auto_refresh_token=False),
            )
            with patch.object(health, "get_supabase_client", return_value=client), patch.dict(
                os.environ, {"SUPABASE_HEALTH_TABLE": "tabela_confirmada", "SUPABASE_HEALTH_COLUMN": "id"}, clear=True
            ), TestClient(app) as api:
                response = api.get("/api/health/database")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].method, "HEAD")
        self.assertEqual(requests[0].url.path, "/rest/v1/tabela_confirmada")
        self.assertEqual(requests[0].url.params["select"], "id")
        self.assertEqual(requests[0].url.params["limit"], "1")
        self.assertNotIn("sb_publishable", response.text)

    def test_failure_returns_generic_503(self):
        # Erros de configuração, rede e permissões não podem vazar pela resposta.
        for error in (SupabaseConfigurationError("segredo"), httpx.ConnectError("segredo"), RuntimeError("segredo")):
            with self.subTest(error=type(error).__name__), patch.object(health, "get_supabase_client", side_effect=error), TestClient(app) as api:
                response = api.get("/api/health/database")
            self.assertEqual(response.status_code, 503)
            self.assertNotIn("segredo", response.text)
            self.assertEqual(response.headers["cache-control"], "no-store")

    def test_missing_or_invalid_identifiers_never_query(self):
        for settings in ({}, {"SUPABASE_HEALTH_TABLE": "tabela", "SUPABASE_HEALTH_COLUMN": "*"}):
            with self.subTest(settings=settings), patch.dict(os.environ, settings, clear=True), patch.object(health, "get_supabase_client") as factory, TestClient(app) as api:
                self.assertEqual(api.get("/api/health/database").status_code, 503)
                factory.return_value.table.assert_not_called()
