from fastapi import APIRouter, status
from pydantic import BaseModel, Field

#cria o roteador de materiais
router = APIRouter(prefix="/api", tags=["Materiais"])

#modela os dados e informações do material
class  MaterialCreate(BaseModel):
    tipo: str = Field(description="Tipo do material (plástico ou metal).", examples=["Plástico"]) # plástico ou metal
    classificacao: str = Field(description="Classificação do material (PET, PEAD, alumínio, ferro).", examples=["PET"]) # PET, PEAD, alumínio, ferro
    destino: str = Field(description="Destino do material (esteira e setor).", examples=["Esteira 01"]) # esteira e setor

#integração ao banco de dados
materiais_db = [
    {"id_material": 1, "tipo": "Plástico", "Classificação": "PET / PEAD", "destino": "Esteira 01"},
    
]

# consulta todo o estoque de materiais
@router.get(
    "/materiais",
    summary="Listar materiais",
    description="Retorna todos os materiais cadastrados no sistema, com tipo, classificação e destino.",
    response_description="Lista de materiais cadastrados.",
)
def listar_materiais():

    return {"materiais": materiais_db}

# cadastrar novo material (EX: em caso de update e ampliação do sistema)
@router.post(
    "/materiais",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar material",
    description="Cadastra um novo tipo de material (útil em caso de ampliação do sistema). O `id_material` é gerado automaticamente de forma sequencial.",
    response_description="Material cadastrado com sucesso.",
    responses={
        201: {
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Material cadastrado com sucesso!",
                        "material": {
                            "id_material": 2,
                            "tipo": "Metal",
                            "classificacao": "Alumínio",
                            "destino": "Esteira 02"
                        }
                    }
                }
            }
        },
        422: {"description": "Erro de validação: campo obrigatório ausente ou com tipo inválido."},
    },
)
def cadastrar_material(material: MaterialCreate):

    novo_material = {
        "id_material": len(materiais_db) + 1, # adiciona +1 fornecedor a lista simulada
        "tipo": material.tipo,
        "classificacao": material.classificacao,
        "destino": material.destino
    }

    materiais_db.append(novo_material) # realiza a contagem da simulação

    return {
        "mensagem": "Material cadastrado com sucesso!",
        "material": novo_material
    }
