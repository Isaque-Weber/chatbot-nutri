from backend.database import SessionLocal, engine, Base
from backend.models import UsuarioAutorizado

# 🔌 Criar uma sessão do banco de dados
db = SessionLocal()

# 📲 Número de telefone que será cadastrado
telefone_teste = "11999999999"

# 🔍 Verificar se o número já existe
usuario_existente = db.query(UsuarioAutorizado).filter_by(telefone=telefone_teste).first()

if not usuario_existente:
    # ➕ Criar um novo usuário autorizado
    novo_usuario = UsuarioAutorizado(telefone=telefone_teste)
    db.add(novo_usuario)
    db.commit()
    print("✅ Usuário cadastrado com sucesso!")
else:
    print("⚠️ Esse número já está cadastrado.")

# 🚪 Fechar a sessão
db.close()
