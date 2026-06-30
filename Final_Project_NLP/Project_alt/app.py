import gradio as gr
from rag_engine import RAGEngine

rag = RAGEngine(directory_path="data_business")

def ask_rag(question):
    answer, sources = rag.answer_question(question)
    return answer, sources

with gr.Blocks(theme=gr.themes.Soft(), title="RAG Business Assistant") as demo:
    gr.Markdown("# 🧠 Assistant RAG Commercial & Réglementaire")
    gr.Markdown("Cette interface interroge la base vectorielle locale pré-chargée avec les documents de **data_business**.")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🏢 Statut du Système")
            gr.Textbox(
                value="Base de données 'data_business' initialisée et indexée avec succès ✅", 
                label="Statut", 
                interactive=False
            )
            gr.Markdown(
                "Les documents comme *Creating_company_france.pdf* et *e-commerce_rules_france.pdf* "
                "sont analysés à l'aide de coupures par phrases (spaCy)."
            )
            
        with gr.Column(scale=2):
            gr.Markdown("### 💬 Poser vos questions")
            question_input = gr.Textbox(
                label="Votre question", 
                placeholder="Ex: What diploma do I need to be a dental surgeon in France?"
            )
            ask_btn = gr.Button("Envoyer la question", variant="primary")
            
            answer_output = gr.Textbox(label="Réponse générée", interactive=False, lines=4)
            sources_output = gr.Textbox(label="Sources utilisées (ChromaDB)", interactive=False, lines=3)

    # Liaison du bouton
    ask_btn.click(fn=ask_rag, inputs=[question_input], outputs=[answer_output, sources_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)