from sqlalchemy import Column, Integer, String
from backend.database.database import Base  # Base é o objeto base que você já configurou

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    telefone = Column(String, unique=True, index=True)
    autorizado = Column(Integer, default=0)  # 0 para não autorizado, 1 para autorizado
    has_comorbidity = Column(Integer, default=0)  # 0 para não tem comorbidade, 1 para tem