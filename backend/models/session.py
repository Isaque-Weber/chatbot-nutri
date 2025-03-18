from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database.database import Base
# Tabela de sessões
class Sessao(Base):
    __tablename__ = 'sessoes'
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))  
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario")  
