"""Gera a documentação OpenAPI da API em docs/openapi.json e docs/openapi.yaml.

Uso (na pasta onde estão main.py e routers/):
    python gerar_openapi.py

O .json é sempre gerado. O .yaml precisa do PyYAML (pip install pyyaml);
se ele não estiver instalado, o script avisa e gera só o .json.
Rode de novo sempre que a API mudar, para manter os arquivos atualizados.
"""
import json
import os

from main import app

os.makedirs("docs", exist_ok=True)
openapi = app.openapi()

with open(os.path.join("docs", "openapi.json"), "w", encoding="utf-8") as arquivo:
    json.dump(openapi, arquivo, ensure_ascii=False, indent=2)
print("docs/openapi.json gerado com sucesso!")

try:
    import yaml
except ImportError:
    print("PyYAML não instalado: openapi.yaml não foi gerado (pip install pyyaml).")
else:
    with open(os.path.join("docs", "openapi.yaml"), "w", encoding="utf-8") as arquivo:
        yaml.safe_dump(openapi, arquivo, allow_unicode=True, sort_keys=False)
    print("docs/openapi.yaml gerado com sucesso!")
