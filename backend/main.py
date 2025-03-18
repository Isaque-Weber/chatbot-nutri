from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from backend.routes.chatbot import router as chatbot_router
from backend.services.taco_retrieval import configure_openai_client
from backend.database import engine, Base, get_db
from backend.database.database import init_db
from backend.routes.usuarios import router as usuarios_router
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

"""Executa ações antes e depois da aplicação rodar."""
print("🚀 Inicializando o banco de dados...")
init_db()  # Inicializa o banco de dados ao iniciar a API

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao servidor de Nutrição!"}

# Incluindo as rotas do chatbot
app.include_router(usuarios_router)  # Incluindo o roteador de usuários
app.include_router(chatbot_router)  # Incluindo o roteador do chatbot

# Exemplo de rota que interage com o banco
@app.get("/db_test/")
def test_db(db: Session = Depends(get_db)):
        # Aqui você pode fazer consultas no banco, por exemplo
        # Exemplo fictício de consulta
    result = db.execute("SELECT 'Testando a conexão'").fetchall()
    return {"db_message": result[0][0]}

# Servindo arquivos estáticos (HTML, CSS, JS)
app.mount("/chat/", StaticFiles(directory="static", html=True), name="static")