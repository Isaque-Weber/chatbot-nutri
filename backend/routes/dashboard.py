from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.user import Usuario
from backend.models.session import Sessao
from backend.models.chat import PerguntaResposta

router = APIRouter()
templates = Jinja2Templates(directory="static")  # Ajuste se a pasta 'templates' estiver em outro lugar

@router.get("/dashboard")
def show_dashboard(request: Request, db: Session = Depends(get_db)):
    total_users = db.query(Usuario).count()
    total_sessions = db.query(Sessao).count()
    total_messages = db.query(PerguntaResposta).count()

    # Renderiza o template 'dashboard.html'
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_users": total_users,
        "total_sessions": total_sessions,
        "total_messages": total_messages
    })

# Exemplo de rota para listar usuários em página HTML
@router.get("/usuarios")
def listar_usuarios_pagina(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return templates.TemplateResponse("usuarios_list.html", {
        "request": request,
        "usuarios": usuarios
    })

# Exemplo de rota para mostrar formulário de cadastro (HTML)
@router.get("/usuarios/cadastrar")
def formulario_cadastro_usuario(request: Request):
    return templates.TemplateResponse("usuarios_form.html", {"request": request})

# Exemplo de rota para processar formulário de cadastro (via POST)
@router.post("/usuarios/cadastrar")
async def cadastrar_usuario_form(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    telefone = form_data.get("telefone")
    nome = form_data.get("nome")
    has_comorbidity = form_data.get("has_comorbidity")  # vai vir como string "0" ou "1"

    # Validações simples
    if not telefone or not nome:
        return templates.TemplateResponse("usuarios_form.html", {
            "request": request,
            "error": "Telefone e Nome são obrigatórios"
        })

    # Verifica se já existe um usuário com esse telefone
    existing_user = db.query(Usuario).filter(Usuario.telefone == telefone).first()
    if existing_user:
        return templates.TemplateResponse("usuarios_form.html", {
            "request": request,
            "error": "Usuário com este telefone já existe"
        })

    # Cria e salva o novo usuário
    autorizado_str = form_data.get("autorizado", "0")  # se não vier nada, fica "0"
    autorizado = int(autorizado_str)

    novo_usuario = Usuario(
        nome=nome,
        telefone=telefone,
        has_comorbidity=int(has_comorbidity),
        autorizado=autorizado
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    # Redireciona de volta para a listagem
    return RedirectResponse(url="/admin/usuarios", status_code=303)

@router.get("/usuarios/editar/{user_id}") # Rota para exibir o formulário de edição
def editar_usuario_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        return templates.TemplateResponse("404.html", {"request": request, "error": "Usuário não encontrado"})

    # Renderiza um template "usuarios_edit.html" com os dados do usuário
    return templates.TemplateResponse("usuarios_edit.html", {
        "request": request,
        "usuario": usuario
    })
    
@router.post("/usuarios/editar") # Rota para processar o formulário de edição
async def atualizar_usuario(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_id = form_data.get("id")
    nome = form_data.get("nome")
    telefone = form_data.get("telefone")
    has_comorbidity = form_data.get("has_comorbidity", "0")
    autorizado = form_data.get("autorizado", "0")

    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "error": "Usuário não encontrado"
        })

    # Atualiza os campos
    usuario.nome = nome
    usuario.telefone = telefone
    usuario.has_comorbidity = int(has_comorbidity)
    usuario.autorizado = int(autorizado)

    db.commit()
    db.refresh(usuario)

    # Redireciona de volta para a listagem
    return RedirectResponse(url="/admin/usuarios", status_code=303)

@router.post("/usuarios/remover") # Rota para remover um usuário
async def remover_usuario(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user_id = form_data.get("id")

    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "error": "Usuário não encontrado"
        })

    db.delete(usuario)
    db.commit()

    return RedirectResponse(url="/admin/usuarios", status_code=303)