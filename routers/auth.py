from fastapi import APIRouter , HTTPException, status
# Modelo movido para schemas; importação preserva o acesso pelo módulo original.
from schemas.auth import LoginRequest

# para autenticação criamos o rotedor aqui
router = APIRouter(prefix="/api", tags=["Autenticação e Segurança"])

# validação do usuário para saber o nível de acesso permitido
@router.post("/login", status_code=status.HTTP_200_OK)
def autenticar_usuario(dados: LoginRequest):

# condicional do admin
    if dados.usuario == "admin" and dados.senha == "123456":
      return {
        "mensagem": "Autenticação realizada com sucesso!",
        "perfil": "ADMINISTRADOR",
        "acesso_liberado": True
    }

# condicional do operador
    elif dados.usuario == "operador" and dados.senha == "123456":
       return {
          "mensagem": "Autenticação realizada com sucesso!",
          "perfil": "OPERADOR",
          "acesso_liberado": True
       }

    else: # em caso de dados incorretos, erro
       raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Acesso negado: Usuário ou senha inválidos."
       )
