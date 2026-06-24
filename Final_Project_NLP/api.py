# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import get_rag_chain
import uvicorn

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

app = FastAPI(
    title="RAG Backend API",
    description="API FastAPI pour interroger le système RAG basé sur LangChain et Qdrant.",
    version="1.0.0"
)

print("Initialisation du système RAG dans FastAPI...")
try:
    rag_chain = get_rag_chain()
    print("Système RAG initialisé avec succès !")
except Exception as e:
    print(f"Erreur d'initialisation RAG : {str(e)}")
    rag_chain = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    """Point d'accès pour poser une question au RAG."""
    if not rag_chain:
        raise HTTPException(status_code=500, detail="La chaîne RAG n'est pas initialisée correctement.")
    
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")
    
    try:
        answer = rag_chain.invoke(payload.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement : {str(e)}")

@app.get("/api/health")
async def health_check():
    """Route de vérification de l'état du serveur."""
    return {"status": "healthy", "rag_initialized": rag_chain is not None}

if __name__ == "__main__":
    uvicorn.run("api.py:app", host="127.0.0.1", port=8000, reload=True)