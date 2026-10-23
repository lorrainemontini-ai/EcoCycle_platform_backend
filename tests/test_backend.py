"""Testes locais de configuração e regressão, sem acesso ao banco."""

import copy
import importlib
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch
from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
from database import supabase_client as db
from scripts import test_supabase_connection as manual


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = Path(self.temp.name) / ".env"
        for mocked in (
            patch.object(db, "ENV_FILE", self.env),
            patch.object(db, "_client", None),
            patch.dict(os.environ, {}, clear=True),
        ):
            mocked.start()
            self.addCleanup(mocked.stop)

    def configure(self):
        os.environ.update(SUPABASE_URL="https://example.supabase.co", SUPABASE_KEY="sb_publishable_teste")

    def test_missing_configuration(self):
        for values in ({}, {"SUPABASE_URL": "https://example.supabase.co"}, {"SUPABASE_KEY": "sb_publishable_teste"}):
            with self.subTest(values=values), patch.dict(os.environ, values, clear=True), patch.object(db, "create_client") as factory:
                with self.assertRaises(db.SupabaseConfigurationError):
                    db.get_supabase_client()
                factory.assert_not_called()

    def test_dotenv_and_environment_priority(self):
        self.env.write_text("SUPABASE_URL=https://example.supabase.co\nSUPABASE_KEY=sb_publishable_arquivo\n", encoding="utf-8")
        os.environ["SUPABASE_KEY"] = "sb_publishable_ambiente"
        with patch.object(db, "create_client") as factory:
            db.get_supabase_client()
            self.assertEqual(factory.call_args.args, ("https://example.supabase.co", "sb_publishable_ambiente"))

    def test_single_client_even_with_concurrent_calls(self):
        self.configure()
        with patch.object(db, "create_client") as factory:
            with ThreadPoolExecutor(max_workers=8) as pool:
                clients = list(pool.map(lambda _: db.get_supabase_client(), range(16)))
            factory.assert_called_once()
            self.assertTrue(all(client is factory.return_value for client in clients))
            options = factory.call_args.kwargs["options"]
            self.assertFalse(options.persist_session)
            self.assertFalse(options.auto_refresh_token)

    def test_invalid_urls_and_privileged_keys(self):
        self.configure()
        for variable, value in (("SUPABASE_URL", "http://example.com"), ("SUPABASE_URL", "https://user:senha@example.com"), ("SUPABASE_URL", "https://example.com/rest/v1"), ("SUPABASE_KEY", "sb_secret_nao_permitida"), ("SUPABASE_KEY", "eyJ_chave_legada")):
            with self.subTest(variable=variable, value=value), patch.dict(os.environ, {variable: value}), patch.object(db, "create_client") as factory:
                with self.assertRaises(db.SupabaseConfigurationError) as caught:
                    db.get_supabase_client()
                self.assertNotIn(value, str(caught.exception))
                factory.assert_not_called()

    def test_factory_failure_is_sanitized_and_retryable(self):
        self.configure()
        with patch.object(db, "create_client", side_effect=RuntimeError("credencial_privada")):
            with self.assertRaises(db.SupabaseConfigurationError) as caught:
                db.get_supabase_client()
            self.assertNotIn("credencial_privada", str(caught.exception))
            self.assertIsNone(caught.exception.__cause__)
        with patch.object(db, "create_client") as factory:
            self.assertIs(db.get_supabase_client(), factory.return_value)

    def test_manual_check_is_head_only(self):
        client = MagicMock()
        with patch.object(manual, "get_supabase_client", return_value=client), patch.object(sys, "argv", ["teste", "--table", "tabela_confirmada", "--column", "coluna_confirmada"]), patch("builtins.print"):
            self.assertEqual(manual.main(), 0)
        client.table.assert_called_once_with("tabela_confirmada")
        client.table.return_value.select.assert_called_once_with("coluna_confirmada", head=True)
        client.table.return_value.select.return_value.limit.assert_called_once_with(1)


class BackendTests(unittest.TestCase):
    def setUp(self):
        mocked = patch.object(db, "create_client", side_effect=AssertionError("Não acessar o banco nos testes."))
        self.factory = mocked.start()
        self.addCleanup(mocked.stop)
        self.app = importlib.import_module("main").app
        self.client = TestClient(self.app)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        for name in ("equipamentos", "fornecedores", "lotes", "materiais", "producao"):
            module = importlib.import_module(f"routers.{name}")
            data = patch.object(module, f"{name}_db", copy.deepcopy(getattr(module, f"{name}_db")))
            data.start()
            self.addCleanup(data.stop)

    def test_startup_imports_and_routes(self):
        self.assertEqual(self.client.get("/").json(), {"mensagem": "API está online e operacional!"})
        expected = {
            "/": {"get"}, "/api/login": {"post"},
            "/api/fornecedores": {"get", "post"}, "/api/materiais": {"get", "post"},
            "/api/lotes": {"get", "post"}, "/api/equipamentos": {"get"},
            "/api/equipamentos/status": {"post"},
            "/api/producao": {"get", "post"}, "/api/producao/dashboard-diario": {"get"},
            "/api/health/database": {"get"},
        }
        paths = self.client.get("/openapi.json").json()["paths"]
        self.assertEqual({path: set(methods) for path, methods in paths.items()}, expected)
        for path, methods in expected.items():
            # O diagnóstico remoto é exercitado separadamente com transporte simulado.
            if "get" in methods and path != "/api/health/database":
                self.assertEqual(self.client.get(path).status_code, 200, path)
        self.assertEqual(self.client.get("/api//producao").status_code, 200)
        self.factory.assert_not_called()

    def test_existing_login_and_validation(self):
        for usuario, perfil in (("admin", "ADMINISTRADOR"), ("operador", "OPERADOR")):
            response = self.client.post("/api/login", json={"usuario": usuario, "senha": "123456"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["perfil"], perfil)
        self.assertEqual(self.client.post("/api/login", json={"usuario": "invalido", "senha": "invalida"}).status_code, 401)
        for path in ("login", "fornecedores", "materiais", "lotes", "equipamentos/status", "producao"):
            self.assertEqual(self.client.post(f"/api/{path}", json={}).status_code, 422)

    def test_existing_writes_and_safety_rules(self):
        payloads = {
            "fornecedores": {"nome": "Teste local", "cnpj": "teste", "contato": "teste"},
            "materiais": {"tipo": "Plástico", "classificacao": "PET", "destino": "Teste"},
            "lotes": {"id_fornecedor": 1, "tipo_material": "PET", "peso_inicial_kg": 10, "observacao": "Teste"},
            "producao": {"turno": "Manhã", "material_processado": "PET", "quantidade_entrada_kg": 10, "quantidade_saida_kg": 8, "refugo_kg": 2},
        }
        for path, payload in payloads.items():
            self.assertEqual(self.client.post(f"/api/{path}", json=payload).status_code, 201)
        result = self.client.post("/api/equipamentos/status", json={"temperatura": 60, "peso_atual_kg": 600, "travada": True})
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(result.json()["alertas_seguranca"]), 3)
        self.assertEqual(result.json()["estado_atual"]["status_operacional"], "ESTEIRA DESLIGADA")
        self.factory.assert_not_called()


if __name__ == "__main__":
    unittest.main()
