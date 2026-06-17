# translator.py
import numpy as np
import ollama
import evaluate
from sentence_transformers import SentenceTransformer


bleu_metric = evaluate.load("bleu")
rouge_metric = evaluate.load("rouge")

def get_cosine_similarity(vec1, vec2):
    """Calcule la similarité cosinus entre deux vecteurs."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
    return float(dot_product / (norm_vec1 * norm_vec2))

def interpret_similarity(score):
    """Interprète le score sémantique selon la grille du notebook."""
    if score >= 0.95:
        return "Nearly identical sentences (Excellent / possibly too similar)"
    elif score >= 0.92:
        return "Very strong semantic preservation (Excellent)"
    elif score >= 0.88:
        return "Good translation/paraphrase (Good)"
    elif score >= 0.84:
        return "Acceptable (Moderate)"
    elif score >= 0.80:
        return "Weak semantic preservation (Poor)"
    else:
        return "Meaning likely changed (Unsatisfactory)"

def generate_translation(prompt_text, target_language="French", model_name="llama3"):
    """Génère une traduction en utilisant Ollama en local."""
    system_instruction = (
        f"You are an expert translator. Translate the following text into {target_language}. "
        "Provide ONLY the translated text as your output. Do not add any introduction, "
        "meta-commentary, or quotes."
    )
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Text to translate: {prompt_text}"},
            ],
            options={"temperature": 0.3},
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Erreur Ollama: {e}")
        return None

# Dans translator.py

def compute_metrics(translated_text, reference_text):
    """Calcule les scores BLEU et ROUGE avec lissage pour éviter le score de 0 sur les phrases courtes."""
    
    bleu_results = bleu_metric.compute(
        predictions=[translated_text], 
        references=[[reference_text]],
        smooth=True
    )
    
    rouge_results = rouge_metric.compute(
        predictions=[translated_text], 
        references=[reference_text]
    )
    
    return {
        "bleu": round(bleu_results["bleu"], 4),
        "rouge1": round(rouge_results["rouge1"], 4),
        "rouge2": round(rouge_results["rouge2"], 4),
        "rougeL": round(rouge_results["rougeL"], 4)
    }