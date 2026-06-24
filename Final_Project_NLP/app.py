import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/api/chat"

def predict(message, history):
    """Fonction Gradio qui fait la passerelle avec l'API FastAPI."""
    payload = {"question": message}

    try:
        response = requests.post(API_URL, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data["answer"]
        else:
            error_detail = response.json().get("detail", "Erreur inconnue")
            return f"Erreur de l'API ({response.status_code}) : {error_detail}"

    except requests.exceptions.ConnectionError:
        return "Impossible de se connecter à l'API FastAPI. Assurez-vous que api.py est bien lancé sur le port 8000."
    except Exception as e:
        return f"Une erreur inattendue est survenue : {str(e)}"

with gr.Blocks() as demo:
    gr.ChatInterface(
        fn=predict,
        title="Mon RAG Personnel (Interface Découplée)",
        description="Posez des questions sur les documents PDF. Les requêtes passent par une API FastAPI dédiée.",
        examples=["Fais-moi un résumé du document", "Quelles sont les informations clés ?"]
    )

if __name__ == "__main__":
    demo.launch(share=False, theme="soft")