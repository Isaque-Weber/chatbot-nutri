from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base

# Tabela para armazenar histórico de mensagens
class PerguntaResposta(Base):
    __tablename__ = 'perguntas_respostas'
    
    id = Column(Integer, primary_key=True, index=True)
    sessao_id = Column(Integer, ForeignKey('sessoes.id'))  
    pergunta = Column(String, index=True)
    resposta = Column(String)
    criado_em = Column(DateTime, default=datetime.utcnow)

    sessao = relationship("Sessao")  
