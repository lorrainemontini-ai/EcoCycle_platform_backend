# O que foi alterado/adicionado – Documentação OpenAPI/Swagger

Este documento explica, de forma simples, **o que mudou** no projeto para adicionar a documentação da API, **o que não mudou** e **o que foi observado e deixado como estava**.

---

## 1. Resumo em uma frase

Foi adicionada **documentação** (textos, descrições e exemplos) às rotas e aos modelos da API. **Nenhuma lógica, regra de negócio, rota ou dado foi alterado.**

---

## 2. Conceitos rápidos

- **OpenAPI:** um padrão para descrever uma API (quais rotas existem, o que recebem e o que devolvem).
- **Swagger UI:** a página visual, gerada a partir do OpenAPI, onde dá para ler e testar as rotas.
- **FastAPI:** já gera o OpenAPI e o Swagger sozinho. O trabalho aqui foi **enriquecer** essa documentação, deixando-a clara e completa.

---

## 3. O que foi adicionado

### 3.1 Nos decoradores das rotas (`@router.get`, `@router.post`)

Em todas as rotas foram acrescentados parâmetros que só afetam a documentação:

| Parâmetro | Para que serve | Onde aparece |
|---|---|---|
| `summary` | Título curto da rota | Lista de rotas no Swagger |
| `description` | Explicação detalhada (regras, campos gerados etc.) | Detalhe da rota |
| `response_description` | O que a resposta de sucesso significa | Detalhe da rota |
| `responses` | Exemplos de resposta e outros códigos (201, 401, 422) | Detalhe da rota |

**Antes:**
```python
@router.get("/fornecedores")
def listar_fornecedores():
```

**Depois:**
```python
@router.get(
    "/fornecedores",
    summary="Listar fornecedores",
    description="Retorna todos os fornecedores cadastrados...",
    response_description="Lista de fornecedores cadastrados.",
    responses={...},
)
def listar_fornecedores():
```

A função em si (o que está abaixo do decorador) **não foi tocada**.

### 3.2 Nos modelos de dados (classes `BaseModel`)

Cada campo ganhou uma descrição e um exemplo usando `Field(...)`:

**Antes:**
```python
class FornecedoresCreate(BaseModel):
    nome: str
```

**Depois:**
```python
class FornecedoresCreate(BaseModel):
    nome: str = Field(description="Nome ou razão social do fornecedor.", examples=["Cooperativa Verde Vida"])
```

Os campos continuam **obrigatórios** e com o **mesmo tipo**. Só passaram a ter texto explicativo e um exemplo pré-preenchido no Swagger.

### 3.3 No `main.py`

Alterações só no último bloco `FastAPI(...)`, que é o que realmente vale na aplicação:

- **`description`** maior, explicando os módulos da API.
- **`openapi_tags`** novo, com a descrição de cada grupo de rotas.
- **Rota `/`** (`home`) com `summary` e `description`.

Os blocos anteriores do arquivo, os imports e todos os `include_router` ficaram exatamente como estavam.

### 3.3.1 Grupos de rotas (tags) descritos

| Tag | Descrição |
|---|---|
| Início | Verificação de disponibilidade da API |
| Autenticação e Segurança | Login e perfil de acesso |
| Fornecedores | Cadastro e consulta de fornecedores |
| Materiais | Cadastro e consulta dos tipos de material |
| Lotes | Registro e consulta dos lotes recebidos |
| Equipamentos | Monitoramento da esteira e regras de segurança |
| Produção e Dashboard | Ciclos de produção e indicadores consolidados |

### 3.4 Arquivos novos

| Arquivo | O que é |
|---|---|
| `gerar_openapi.py` | Script que gera os arquivos OpenAPI. Não faz parte da API, só é executado manualmente |
| `docs/openapi.json` | Documentação OpenAPI em JSON |
| `docs/openapi.yaml` | Documentação OpenAPI em YAML (gerado se o PyYAML estiver instalado) |
| `docs/README.md` | Guia de acesso, uso e manutenção |
| `docs/ALTERACOES.md` | Este documento |

---

## 4. Tabela de arquivos

| Arquivo | Situação | O que mudou |
|---|---|---|
| `main.py` | Alterado | Só documentação (descrição, tags, `home`) |
| `routers/auth.py` | Alterado | Só documentação |
| `routers/fornecedores.py` | Alterado | Só documentação |
| `routers/materiais.py` | Alterado | Só documentação |
| `routers/lotes.py` | Alterado | Só documentação |
| `routers/equipamentos.py` | Alterado | Só documentação |
| `routers/producao.py` | Alterado | Só documentação |
| `routers/__init__.py` | **Sem alteração** | – |
| `gerar_openapi.py` | Novo | Script gerador |
| `docs/*` | Novo | Documentação |

---

## 5. O que NÃO foi alterado

- O corpo de todas as funções (`if`, cálculos, retornos).
- Os caminhos, métodos HTTP e `status_code` das rotas.
- Os nomes e tipos dos campos dos modelos (todos continuam obrigatórios).
- Os dados simulados (`fornecedores_db`, `lotes_db`, `materiais_db`, `equipamentos_db`, `producao_db`).
- Os comentários originais do código.
- As regras de negócio (limites da esteira, cálculo do dashboard etc.).

Isso foi conferido comparando os arquivos originais com os novos e testando a API: login, alertas da esteira, produção e dashboard respondem como antes.

---

## 6. O que foi observado e deixado como estava

Durante a leitura do código foram encontrados pontos que **não foram corrigidos**, porque o objetivo era apenas documentar. Ficam registrados para a equipe decidir:

| # | Arquivo | Observação |
|---|---|---|
| 1 | `main.py` | Contém várias versões da aplicação concatenadas. Funciona porque o `auth` é importado no primeiro bloco e o último `app` sobrescreve os anteriores, mas o ideal é manter só uma versão |
| 2 | `routers/producao.py` | A rota de listagem está como `"//producao"` (barra dupla), então aparece como `/api//producao` no Swagger. O esperado seria `/producao` |
| 3 | `routers/equipamentos.py` | O dicionário inicial tem `peso_atual_kh` (typo), mas a atualização grava `peso_atual_kg`. Depois da primeira atualização, o GET devolve as duas chaves |
| 4 | `routers/lotes.py` | O item inicial usa `"tipo-material"` (hífen), mas o cadastro usa `"tipo_material"` |
| 5 | `routers/materiais.py` | O item inicial usa `"Classificação"`, mas o cadastro usa `"classificacao"` |
| 6 | `routers/producao.py` | O item inicial usa `material_processados` (plural), mas o cadastro usa `material_processado` |
| 7 | `routers/fornecedores.py` | A função se chama `cafastrar_fornecedores` (typo). O nome vai para o `operationId` do OpenAPI |
| 8 | `routers/auth.py` | Usuário e senha estão fixos no código e o login não devolve token. Nos exemplos do Swagger a senha real **não** foi usada |

> Os itens 2 a 6 aparecem na documentação gerada porque ela reflete o código. Quando forem corrigidos, basta rodar `python gerar_openapi.py` de novo e revisar os exemplos de resposta.

---

## 7. Como a equipe pode revisar esta alteração

1. Compare os arquivos alterados com a `main` (diff do Git). Em cada router, só devem aparecer linhas de documentação nos decoradores e nos campos.
2. Rode a API e abra `http://127.0.0.1:8000/docs`.
3. Teste algumas rotas pelo **Try it out** e confirme que o comportamento é o de sempre.
