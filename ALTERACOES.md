# Registro das alterações

## Organização do projeto

- `main.py`: removidas as inicializações duplicadas. Mantida uma aplicação FastAPI,
  com a mesma identificação e resposta da rota raiz.
- `routers/__init__.py`: registro único dos roteadores, simplificando a entrada.
- `schemas/__init__.py` e `schemas/auth.py`, `equipamentos.py`, `fornecedores.py`,
  `lotes.py`, `materiais.py`, `producao.py`: modelos Pydantic extraídos das rotas,
  mantendo nomes, campos e comportamento de validação.
- `routers/auth.py`, `equipamentos.py`, `fornecedores.py`, `lotes.py`, `materiais.py`
  e `producao.py`: importam os modelos separados. Comentários identificam o
  armazenamento simulado; os dados e regras originais foram preservados.
- `routers/producao.py`: adicionado GET `/api/producao`. O caminho original com
  duas barras permanece como alias, sem aparecer no OpenAPI.

## Preparação do Supabase e diagnóstico

- `database/__init__.py`: identifica o pacote de acesso ao banco.
- `database/supabase_client.py`: carrega `.env`, respeita prioridade do ambiente,
  valida URL e chave publicável e cria um cliente por processo sob bloqueio.
  Erros não expõem credenciais; sessões não são persistidas nem renovadas.
  Acrescentado tempo de espera de cinco segundos para a API de dados.
- `database/health.py`: lê a tabela e coluna configuradas no servidor e executa
  somente HEAD, com limite de uma linha. Não pressupõe o esquema instalado.
- `routers/health.py`: GET `/api/health/database` retorna 200 em caso de sucesso
  ou 503 genérico em caso de falha. Não retorna registros e impede cache HTTP.
- `.env.example`: configurações vazias e comentários sobre cada grupo de variáveis,
  incluindo a tabela e a coluna do diagnóstico.
- `.gitignore`: ignora ambientes virtuais, credenciais e novos caches Python.
- `scripts/__init__.py` e `scripts/test_supabase_connection.py`: alternativa manual
  de diagnóstico HEAD com tabela/coluna explícitas, sem exibição de registros.

## Dependências, testes e documentação

- `requirements.txt`: dependências diretas com versões verificadas.
- `requirements.lock.txt`: registro das versões transitivas instaladas na `.venv`.
  É um arquivo gerado; os comentários explicativos ficam neste documento.
- `tests/test_backend.py`: configuração, criação concorrente do cliente, falhas
  sanitizadas e regressão dos contratos e regras originais. Atualizado para o
  registro central de rotas e o alias de produção.
- `tests/test_health.py`: diagnóstico com transporte HTTP simulado, resposta 200,
  resposta 503, proteção de mensagens e ausência de consulta com nomes inválidos.
- `README.md`: instalação local, uso do cliente, estrutura, endpoints, diagnóstico,
  testes, divergências dos diagramas e pendências de autenticação/RLS.
- `ALTERACOES.md`: este registro explica todas as mudanças das duas etapas.

Os blocos alterados e os novos módulos possuem comentários ou docstrings em
português. Nenhuma tabela foi criada ou modificada; as rotas de negócio continuam
em memória. A autenticação simulada ainda precisa ser substituída por uma solução
validada antes de liberar acesso a dados reais. Nenhum commit foi realizado.
