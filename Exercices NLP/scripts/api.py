# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import translator

app = FastAPI(title="API de Traduction et d'Évaluation", version="2.0")

print("Chargement du modèle Sentence-Transformers...")
eval_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class TranslationRequest(BaseModel):
    text: str
    target_lang: str = "French"
    model: str = "llama3"
    reference: str = ""

@app.post("/translate")
async def process_translation(request: TranslationRequest):
    translated_text = translator.generate_translation(request.text, request.target_lang, request.model)
    
    if not translated_text:
        raise HTTPException(status_code=500, detail="Erreur lors de la génération de la traduction.")

    embeddings = eval_model.encode([request.text, translated_text])
    similarity_score = translator.get_cosine_similarity(embeddings[0], embeddings[1])
    verdict = translator.interpret_similarity(similarity_score)
    
    metrics = {"bleu": 0.0, "rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
    if request.reference.strip():
        metrics = translator.compute_metrics(translated_text, request.reference)
        
    return {
        "translated_text": translated_text,
        "similarity_score": round(similarity_score, 4),
        "verdict": verdict,
        "metrics": metrics
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)