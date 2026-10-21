from fastapi import APIRouter, status
from pydantic import BaseModel

#cria o roteador de materiais
router = APIRouter(prefix="/api", tags=["Materiais"])

#modela os dados e informações do material
class  MaterialCreate(BaseModel):
    tipo: str # plástico ou metal
    classificacao: str # PET, PEAD, alumínio, ferro
    destino: str # esteira e setor

#integração ao banco de dados
materiais_db = [
    {"id_material": 1, "tipo": "Plástico", "Classificação": "PET / PEAD", "destino": "Esteira 01"},
    
]

# consulta todo o estoque de materiais
@router.get("/materiais")
def listar_materiais():

    return {"materiais": materiais_db}

# cadastrar novo material (EX: em caso de update e ampliação do sistema)
@router.post("/materiais", status_code=status.HTTP_201_CREATED)
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