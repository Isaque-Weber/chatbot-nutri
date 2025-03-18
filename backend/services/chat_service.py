from sqlalchemy.orm import Session
from backend.models.chat import PerguntaResposta

def salvar_chat(db: Session, pergunta: str, resposta: str):
    chat = PerguntaResposta(pergunta=pergunta, resposta=resposta)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
