import gradio as gr
from rag_engine import RAGEngine

# Initialisation unique de notre moteur RAG au démarrage
rag = RAGEngine()

def upload_and_index(file):
    if file is None:
        return "Veuillez sélectionner un fichier PDF valide."
    # Appelle la logique d'extraction et d'embedding
    status = rag.process_pdf(file.name)
    return status

def ask_rag(question):
    # Appelle la logique de recherche vectorielle et de génération LLM
    answer, sources = rag.answer_question(question)
    return answer, sources

# Construction de l'interface graphique Gradio
with gr.Blocks(theme=gr.themes.Soft(), title="RAG PDF Assistant") as demo:
    gr.Markdown("# 🧠 Assistant RAG Document-PDF")
    gr.Markdown("Téléversez un document PDF pour l'analyser localement avec **Hugging Face** et poser vos questions.")
    
    with gr.Row():
        # Colonne de gauche : Chargement du fichier
        with gr.Column(scale=1):
            gr.Markdown("### 1. Préparation du document")
            pdf_input = gr.File(label="Téléverser un fichier PDF", file_types=[".pdf"])
            upload_btn = gr.Button("Indexer le PDF", variant="primary")
            upload_status = gr.Textbox(label="Statut de l'indexation", interactive=False)
            
        # Colonne de droite : Chat & Réponses
        with gr.Column(scale=2):
            gr.Markdown("### 2. Poser vos questions")
            question_input = gr.Textbox(label="Votre question", placeholder="Ex: De quoi parle la section 3 ?")
            ask_btn = gr.Button("Envoyer la question", variant="secondary")
            
            answer_output = gr.Textbox(label="Réponse générée (Google Flan-T5-Large)", interactive=False, lines=4)
            sources_output = gr.Textbox(label="Sources utilisées (ChromaDB Vector Store)", interactive=False, lines=3)

    # Liaisons des événements de boutons aux fonctions Python
    upload_btn.click(fn=upload_and_index, inputs=[pdf_input], outputs=[upload_status])
    ask_btn.click(fn=ask_rag, inputs=[question_input], outputs=[answer_output, sources_output])

# Lancement de l'application
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)