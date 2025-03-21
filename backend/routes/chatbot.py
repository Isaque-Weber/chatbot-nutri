import markdown2
from pydantic import BaseModel
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
    telefone: str
    pergunta: str
    def normalizar_telefone(self):
        return self.telefone.replace("+", "").strip()

class VerificacaoRequest(BaseModel):
    telefone: str

# Inicializa o Assistant apenas uma vez (ao iniciar o servidor)
assistant = process_pdf_and_create_assistant("./backend/data/taco.pdf")

usuarios_autorizados = {"5511999999999", "+5511999999999"}


# Função para recuperar as últimas interações do banco de dados
def get_last_messages(db: Session, limit=5):
    """Busca as últimas mensagens armazenadas no banco de dados."""
    return db.query(PerguntaResposta).order_by(PerguntaResposta.id.desc()).limit(limit).all()

# Rota para consultar o PDF via Assistant
@router.post("/consultar")
async def consultar_alimento(request: ConsultaRequest, db: Session = Depends(get_db)):
    # Verifica se o usuário está autorizado
    usuario = db.query(Usuario).filter(Usuario.telefone == "+5511999999999").first()  # 📌 Ajuste para pegar o telefone real

    telefone_normalizado = request.normalizar_telefone()
    print("Número recebido:", request.telefone)  # Debugging


    if telefone_normalizado not in usuarios_autorizados:
        print(f"Usuário {telefone_normalizado} não autorizado!")
        return {"erro": f"Usuário {telefone_normalizado} não autorizado para acessar o chatbot."}

    print(f"Usuário {telefone_normalizado} autorizado!")
    # 2) Captura se ele tem comorbidade
    possui_comorbidade = (usuario.has_comorbidity == 1)
    
    # 3) Monta instruções extras se tiver comorbidade
    if possui_comorbidade:
        extra_contexto = (
            "ATENÇÃO: Este usuário possui uma comorbidade. "
            "Fornecer orientações alimentares mais cautelosas, "
            "considerando possíveis restrições nutricionais."
        )
    else:
        extra_contexto = ""

    
    pergunta = request.pergunta

    # 4) Recupera histórico, monta contexto da conversa
    historic = get_last_messages(db)
    contexto_historico = "\n".join([
        f"Usuário: {msg.pergunta}\nAssistente: {msg.resposta}" for msg in historic
    ])

    # 5) Combina tudo em uma pergunta com contexto adicional
    pergunta_com_contexto = f"{contexto_historico}\n{extra_contexto}\nUsuário: {request.pergunta}"

    # 🔍 Envia a pergunta com contexto para a IA
    assistant_id = 'asst_6FrcxlrCjmX5P4ovOIU2Fcwv'
    resposta = query_assistant(assistant_id, pergunta_com_contexto)

    # 💾 Salva a nova interação no banco
    salvar_chat(db, request.pergunta, resposta)  # 📌 Agora usamos a função otimizada!

    return {"resposta": resposta}

@router.post("/verificar_acesso")
def verificar_acesso(request: VerificacaoRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.telefone == request.telefone).first()

    if usuario:
        return {"acesso": True, "mensagem": "Acesso autorizado!"}
    else:
        raise HTTPException(status_code=403, detail="Acesso negado! Número não autorizado.")
