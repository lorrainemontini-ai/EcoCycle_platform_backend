# Documentação da API – EcoCycle (Backend Equipe 2)

Este guia explica **como acessar**, **como usar** e **como manter** a documentação OpenAPI/Swagger da API EcoCycle.

> A API ainda está em desenvolvimento. Esta documentação acompanha o código e deve ser atualizada junto com ele (veja a seção [Manutenção](#4-manutenção-quando-alterar-a-api)).

---

## 1. O que é a documentação

A API usa o **FastAPI**, que gera sozinho a documentação no padrão **OpenAPI**. Ela fica disponível de duas formas:

| Forma | Para que serve |
|---|---|
| **Swagger UI** (`/docs`) | Página interativa: dá para ler e **testar** as rotas direto no navegador |
| **Arquivo OpenAPI** (`docs/openapi.json` e `docs/openapi.yaml`) | Arquivo para entregar, versionar ou importar em outras ferramentas |

A documentação é **gerada a partir do código**. Se o código mudar, o Swagger ao vivo muda junto. Só os textos e os exemplos escritos à mão nos decoradores precisam ser revisados por quem altera a rota.

---

## 2. Como acessar

### 2.1 Instalar as dependências

```bash
pip install fastapi uvicorn
pip install pyyaml        # opcional: só para gerar o openapi.yaml
```

### 2.2 Rodar a API

Na pasta raiz do projeto (onde está o `main.py`):

```bash
uvicorn main:app --reload
```

> Rode sempre da pasta raiz, porque o `main.py` importa `from routers import ...`.

### 2.3 Abrir a documentação

Com a API rodando copie o endereço e cole no navegador:

| O quê | Endereço |
|---|---|
| Swagger UI (interativo) | http://127.0.0.1:8000/docs |
| OpenAPI em JSON (gerado ao vivo) | http://127.0.0.1:8000/openapi.json |

---

### 2.4 Como parar a API

1. Clique na janela do terminal onde o `uvicorn` está rodando.
2. Aperte **CTRL+C**.
3. Quando o terminal voltar ao prompt normal (por exemplo, `PS C:\...>`), a API foi encerrada e o `/docs` deixa de abrir.

Para subir de novo, rode `uvicorn main:app --reload`.

**Se aparecer um texto longo com `Traceback` e `KeyboardInterrupt` ao parar**

```
Process SpawnProcess-1:
Traceback (most recent call last):
  ...
KeyboardInterrupt
INFO:     Stopping reloader process [84972]
```

Isso é normal e **não é um erro da API**. O `KeyboardInterrupt` é o próprio CTRL+C que você apertou. No Windows, o `uvicorn` com `--reload` mostra esse texto ao ser interrompido. A linha `Stopping reloader process` confirma que ele encerrou.

**Se o CTRL+C não funcionar:** aperte de novo ou feche o terminal. Se a API continuar no ar depois disso, encerre o processo do Python pelo Gerenciador de Tarefas.

---

## 3. Como usar o Swagger (`/docs`)

1. As rotas aparecem agrupadas por **tags** (Autenticação e Segurança, Fornecedores, Materiais, Lotes, Equipamentos, Produção e Dashboard, Início).
2. Clique em uma rota para abrir os detalhes: descrição, campos esperados, exemplos e códigos de resposta.
3. Para **testar**: clique em **Try it out**, preencha (ou ajuste) o JSON de exemplo e clique em **Execute**.
4. Veja o resultado em **Server response**: código de status e corpo da resposta.

**Códigos de resposta que você vai encontrar**

| Código | Significado |
|---|---|
| `200` | Consulta ou operação realizada com sucesso |
| `201` | Registro criado com sucesso (cadastros e produção) |
| `401` | Usuário ou senha inválidos (login) |
| `422` | Erro de validação: campo obrigatório ausente ou com tipo errado |

> **Atenção:** os dados da API são simulados em memória. Ao reiniciar o servidor, os cadastros feitos nos testes são perdidos.

---

## 4. Manutenção: quando alterar a API

A documentação mora **dentro do código**, nos arquivos que você já edita. Veja onde mexer em cada caso.

### 4.1 Onde está cada parte da documentação

| O que documentar | Onde fica |
|---|---|
| Título, descrição geral e descrição dos grupos (tags) | `main.py` → `FastAPI(...)` e `openapi_tags` |
| Título, descrição e exemplos de uma rota | `routers/<arquivo>.py` → no decorador da rota (`@router.get(...)`, `@router.post(...)`) |
| Descrição e exemplo de cada campo enviado | `routers/<arquivo>.py` → nas classes `BaseModel`, em `Field(description=..., examples=[...])` |

### 4.2 O que fazer em cada tipo de alteração

| Se você... | Então... |
|---|---|
| Mudou a **lógica interna** sem mudar o que a rota recebe ou devolve | Nada a fazer na documentação |
| **Adicionou ou removeu um campo** no modelo (`BaseModel`) | Atualize o `Field(...)` do campo e o **exemplo de resposta** da rota, se ele mostrar esse campo |
| **Mudou o que a rota devolve** | Atualize o bloco `responses` (exemplo) da rota |
| **Criou uma rota nova** | Adicione `summary`, `description` e `responses` no decorador (modelo abaixo) |
| **Mudou o caminho, o método ou o status code** | O Swagger muda sozinho. Revise `summary`/`description` se citarem o caminho antigo |
| **Criou um router novo** (novo arquivo em `routers/`) | Inclua em `main.py` (`include_router`) e adicione a tag em `openapi_tags` |
| **Mudou as regras de negócio** (ex.: limites da esteira) | Atualize o texto do `description` da rota que cita essas regras |

### 4.3 Modelo para documentar uma rota nova

```python
@router.post(
    "/exemplo",
    status_code=status.HTTP_201_CREATED,
    summary="Frase curta do que a rota faz",
    description="Explicação mais completa: regras, campos gerados automaticamente etc.",
    response_description="O que a resposta de sucesso representa.",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {"mensagem": "Criado com sucesso!"}
                }
            }
        },
        422: {"description": "Erro de validação: campo obrigatório ausente ou com tipo inválido."},
    },
)
def criar_exemplo(dados: ExemploCreate):
    ...
```

### 4.4 Modelo para documentar um campo

```python
class ExemploCreate(BaseModel):
    nome: str = Field(description="Nome do item.", examples=["Item A"])
```

O campo continua **obrigatório**. A documentação só acrescenta a descrição e o exemplo.

### 4.5 Gerar os arquivos `openapi.json` e `openapi.yaml` de novo

Depois de alterar a API, regenere os arquivos da pasta `docs/`:

```bash
python gerar_openapi.py
```

- O `openapi.json` é sempre gerado.
- O `openapi.yaml` só é gerado se o PyYAML estiver instalado (`pip install pyyaml`). Se não estiver, o script avisa e gera só o JSON.

> O Swagger (`/docs`) não depende desses arquivos. Eles servem para entregar, versionar ou importar em outra ferramenta. Gere-os quando a versão da API estiver estável.

### 4.6 Checklist antes de enviar uma alteração

- [ ] A API sobe sem erro (`uvicorn main:app --reload`)
- [ ] O `/docs` abre e a rota alterada aparece correta
- [ ] Testei a rota pelo **Try it out**
- [ ] Os exemplos de resposta batem com o que a rota realmente devolve
- [ ] Rodei `python gerar_openapi.py` e commitei os arquivos de `docs/`

---

## 5. Importar a documentação em outras ferramentas

O arquivo `docs/openapi.json` (ou `.yaml`) pode ser importado em:

- **Postman:** *Import* → selecione o arquivo → a coleção com todas as rotas é criada.
- **Insomnia:** *Create → Import* → selecione o arquivo.
- **Swagger Editor** (editor.swagger.io): *File → Import file*.

---

## 6. Problemas comuns

| Problema | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'routers'` | Servidor iniciado fora da pasta raiz | Rode o `uvicorn` na pasta onde está o `main.py` |
| `/docs` não abre | API não está rodando ou a porta é outra | Confira o terminal e o endereço mostrado pelo `uvicorn` |
| Swagger abre em branco | Sem internet (o `/docs` carrega o visual de um CDN) | Conecte à internet. O `/openapi.json` e os arquivos da pasta `docs/` funcionam sem internet |
| `openapi.yaml` não foi gerado | PyYAML não instalado | `pip install pyyaml` e rode o script de novo |
| Exemplo do Swagger não bate com a resposta real | Resposta mudou e o exemplo não foi atualizado | Atualize o bloco `responses` da rota |
| `Traceback` com `KeyboardInterrupt` ao parar a API | É o CTRL+C sendo registrado (comum no Windows com `--reload`) | Nenhuma. É normal. Veja a seção 2.4 |

---

## 7. Estrutura do projeto

```
EcoCycle/
├── main.py                 # cria a aplicação e registra os routers
├── gerar_openapi.py        # gera docs/openapi.json e docs/openapi.yaml
├── routers/
│   ├── __init__.py
│   ├── auth.py             # login e perfil de acesso
│   ├── fornecedores.py
│   ├── materiais.py
│   ├── lotes.py
│   ├── equipamentos.py     # esteira e regras de segurança
│   └── producao.py         # produção e dashboard diário
└── docs/
    ├── README.md           # este guia
    ├── ALTERACOES.md       # o que foi adicionado na documentação
    ├── openapi.json
    └── openapi.yaml
```
