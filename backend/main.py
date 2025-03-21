from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from backend.routes.chatbot import router as chatbot_router
from backend.routes.usuarios import router as usuarios_router
from backend.routes.dashboard import router as dashboard_router  # <== IMPORTANTE
from backend.database.database import init_db

print("🚀 Inicializando o banco de dados...")
init_db()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao servidor de Nutrição!"}

# Montar arquivos estáticos
app.mount("/chat/", StaticFiles(directory="static"), name="static")
# Ou, se quiser manter /chat/ como prefixo, ok também.
# app.mount("/chat", StaticFiles(directory="static"), name="static")

# Incluindo rotas
app.include_router(usuarios_router, prefix="/api")
app.include_router(chatbot_router, prefix="/chatbot")
app.include_router(dashboard_router, prefix="/admin")  # <== ADICIONA O DASHBOARD