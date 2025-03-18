from sqlalchemy.orm import Session
from backend.models.chat import Chat

def salvar_chat(db: Session, pergunta: str, resposta: str):
    chat = Chat(pergunta=pergunta, resposta=resposta)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
