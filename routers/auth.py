from fastapi import APIRouter , HTTPException, status 
from pydantic import BaseModel

# para autenticação criamos o rotedor aqui
router = APIRouter(prefix="/api", tags=["Autenticação e Segurança"])

# exigência de que o 'usuário' e 'senha' sejam preenchidos
class LoginRequest(BaseModel):
    usuario: str
    senha: str

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