import markdown2
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.services.taco_retrieval import process_pdf_and_create_assistant, query_assistant
from backend.database.database import get_db
from backend.services.chat_service import salvar_chat  # ⬅️ Importando a função que salva no banco
from sqlalchemy.orm import Session
from backend.models.user import Usuario  # ⬅️ Importando o modelo do usuário
from backend.models.chat import PerguntaResposta  # ⬅️ Importando o modelo do chat

router = APIRouter()

# Modelo para a consulta
class ConsultaRequest(BaseModel):
    pergunta: str

class VerificacaoRequest(BaseModel):
    telefone: str

# Inicializa o Assistant apenas uma vez (ao iniciar o servidor)
assistant = process_pdf_and_create_assistant("./backend/data/taco.pdf")

# Função para recuperar as últimas interações do banco de dados
def get_last_messages(db: Session, limit=5):
    """Busca as últimas mensagens armazenadas no banco de dados."""
    return db.query(PerguntaResposta).order_by(PerguntaResposta.id.desc()).limit(limit).all()

# Rota para consultar o PDF via Assistant
@router.post("/consultar")
async def consultar_alimento(request: ConsultaRequest, db: Session = Depends(get_db)):
    # Verifica se o usuário está autorizado
    usuario = db.query(Usuario).filter(Usuario.telefone == "11999999999").first()  # 📌 Ajuste para pegar o telefone real

    if not usuario or not usuario.autorizado:
        return {"erro": "Usuário não autorizado para acessar o chatbot."}

    assistant_id = 'asst_6FrcxlrCjmX5P4ovOIU2Fcwv'
    pergunta = request.pergunta

    # 🔄 Recupera as últimas mensagens para o contexto
    historic = get_last_messages(db)

    # 🔗 Monta o contexto da conversa
    contexto = "\n".join([f"Usuário: {msg.pergunta}\nAssistente: {msg.resposta}" for msg in historic])
    pergunta_com_contexto = f"{contexto}\nUsuário: {pergunta}"

    # 🔍 Envia a pergunta com contexto para a IA
    resposta = query_assistant(assistant_id, pergunta_com_contexto)

    # 💾 Salva a nova interação no banco
    salvar_chat(db, pergunta, resposta)  # 📌 Agora usamos a função otimizada!

    return {"resposta": resposta}

@router.post("/verificar_acesso")
def verificar_acesso(request: VerificacaoRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.telefone == request.telefone).first()

    if usuario:
        return {"acesso": True, "mensagem": "Acesso autorizado!"}
    else:
        raise HTTPException(status_code=403, detail="Acesso negado! Número não autorizado.")
