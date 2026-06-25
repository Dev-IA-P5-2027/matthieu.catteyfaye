import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import get_rag_chain
import uvicorn
from contextlib import asynccontextmanager


app_state = {"rag_chain": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initialisation du système RAG au démarrage de FastAPI...")
    try:
        app_state["rag_chain"] = get_rag_chain()
        print("Système RAG initialisé avec succès !")
    except Exception as e:
        print(f"Erreur critique lors de l'initialisation RAG : {str(e)}")
        traceback.print_exc()
        app_state["rag_chain"] = None

    yield

    print("Fermeture de l'application FastAPI.")

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

app = FastAPI(
    title="RAG Backend API",
    description="API FastAPI pour interroger le système RAG basé sur LangChain et Qdrant.",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    rag_chain = app_state["rag_chain"]

    if not rag_chain:
        raise HTTPException(status_code=500, detail="La chaîne RAG n'est pas initialisée correctement.")

    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")

    try:
        answer = rag_chain.invoke(payload.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        print("=== ERREUR LORS DE L'INVOCATION DU RAG ===")
        traceback.print_exc()
        print("==========================================")
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement : {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "rag_initialized": app_state["rag_chain"] is not None}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)