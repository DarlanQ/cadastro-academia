from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, Aluno
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir que o frontend acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para criar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota: listar todos os alunos
@app.get("/alunos")
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

# Rota: criar um novo aluno
@app.post("/alunos")
def criar_aluno(aluno: dict, db: Session = Depends(get_db)):
    novo_aluno = Aluno(**aluno)
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

# Rota: atualizar aluno
@app.put("/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: int, dados: dict, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    for key, value in dados.items():
        setattr(aluno, key, value)
    db.commit()
    db.refresh(aluno)
    return aluno

# Rota: deletar aluno
@app.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return {"ok": True}







from fastapi import FastAPI, Depends, HTTPException, Request
# ... (outros imports já existentes)

# (todo o código já existente permanece)

# Rota de login simples (autenticação)
@app.post("/login")
async def login(request: Request):
    dados = await request.json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if usuario == "admin" and senha == "1234":
        return {"mensagem": "Login bem-sucedido"}
    else:
        return {"erro": "Usuário ou senha inválidos"}
