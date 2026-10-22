from fastapi import APIRouter , HTTPException, status 
from pydantic import BaseModel, Field

# para autenticação criamos o rotedor aqui
router = APIRouter(prefix="/api", tags=["Autenticação e Segurança"])

# exigência de que o 'usuário' e 'senha' sejam preenchidos
class LoginRequest(BaseModel):
    usuario: str = Field(description="Nome de usuário. Perfis existentes: `admin` e `operador`.", examples=["operador"])
    senha: str = Field(description="Senha do usuário.", examples=["sua_senha"])

# validação do usuário para saber o nível de acesso permitido
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Autenticar usuário",
    description=(
        "Valida `usuario` e `senha` e devolve o perfil de acesso.\n\n"
        "Perfis possíveis: **ADMINISTRADOR** e **OPERADOR**."
    ),
    response_description="Autenticação realizada com sucesso.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Autenticação realizada com sucesso!",
                        "perfil": "OPERADOR",
                        "acesso_liberado": True
                    }
                }
            }
        },
        401: {
            "description": "Usuário ou senha inválidos.",
            "content": {
                "application/json": {
                    "example": {"detail": "Acesso negado: Usuário ou senha inválidos."}
                }
            }
        },
    },
)
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
