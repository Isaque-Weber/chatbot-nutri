from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from pydantic import BaseModel
from backend.models.user import Usuario  # Importe o modelo de usuário da pasta 'models'

router = APIRouter()

# Modelo para criar/atualizar usuários
class UsuarioCreate(BaseModel):
    telefone: str

# Endpoint para cadastrar um novo usuário
@router.post("/usuarios/cadastrar")
async def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.telefone == usuario.telefone).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Este número já está cadastrado.")
    
    novo_usuario = Usuario(telefone=usuario.telefone)
    db.add(novo_usuario)
    db.commit()
    
    return {"message": f"Usuário {usuario.telefone} cadastrado com sucesso!"}

# Endpoint para remover um usuário
@router.delete("/usuarios/remover")
async def remover_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.telefone == usuario.telefone).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    db.delete(existing_user)
    db.commit()
    
    return {"message": f"Usuário {usuario.telefone} removido com sucesso!"}

# Endpoint para listar todos os usuários cadastrados
@router.get("/usuarios")
async def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return {"usuarios": usuarios}

# Endpoint para buscar um usuário pelo telefone
@router.get("/usuarios/{telefone}")
async def buscar_usuario(telefone: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.telefone == telefone).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    return {"usuario": usuario}
