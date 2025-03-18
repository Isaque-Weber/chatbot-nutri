import markdown2
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.services.taco_retrieval import process_pdf_and_create_assistant, query_assistant
from backend.database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter()

# Modelo para a consulta
class ConsultaRequest(BaseModel):
    pergunta: str

class VerificacaoRequest(BaseModel):
    telefone: str

# Inicializa o Assistant apenas uma vez (ao iniciar o servidor)
assistant = process_pdf_and_create_assistant("./backend/data/taco.pdf")

# Função para recuperar as últimas interações do banco de dados
def get_last_messages(db, limit=5):
    """Busca as últimas mensagens armazenadas no banco de dados."""
    result = db.execute(
        text("SELECT pergunta, resposta FROM perguntas_respostas ORDER BY id DESC LIMIT :limit"),
        {"limit": limit}
    )
    return result.fetchall()


# Rota para consultar o PDF via Assistant
@router.post("/consultar")
async def consultar_alimento(request: ConsultaRequest, db: Session = Depends(get_db)):
    # Verifica se o usuário está autorizado
    usuario = db.execute(
        text("SELECT autorizado FROM usuarios WHERE telefone = :telefone"),
        {"telefone": "11999999999"}  # 🚨 Aqui depois você pega o telefone real do usuário que enviou a mensagem no WhatsApp
    ).fetchone()

    if not usuario or not usuario[0]:
        return {"erro": "Usuário não autorizado para acessar o chatbot."}

    assistant_id = 'asst_6FrcxlrCjmX5P4ovOIU2Fcwv'
    pergunta = request.pergunta

    # 🔄 Recupera as últimas mensagens para o contexto
    historic = get_last_messages(db)

    # 🔗 Monta o contexto da conversa
    contexto = "\n".join([f"Usuário: {msg[0]}\nAssistente: {msg[1]}" for msg in historic])
    pergunta_com_contexto = f"{contexto}\nUsuário: {pergunta}"

    # 🔍 Envia a pergunta com contexto para a IA
    resposta = query_assistant(assistant_id, pergunta_com_contexto)

    # 💾 Salva a nova interação no banco
    db.execute(
        text("INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (:pergunta, :resposta)"),
        {"pergunta": request.pergunta, "resposta": resposta}
    )
    db.commit()

    return {"resposta": resposta}

@router.post("/verificar_acesso")
def verificar_acesso(request: VerificacaoRequest, db: Session = Depends(get_db)):
    usuario = db.execute(
        text("SELECT * FROM usuarios_autorizados WHERE telefone = :telefone"),
        {"telefone": request.telefone}
    ).fetchone()

    if usuario:
        return {"acesso": True, "mensagem": "Acesso autorizado!"}
    else:
        raise HTTPException(status_code=403, detail="Acesso negado! Número não autorizado.")