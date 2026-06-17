# app_interface.py
import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/translate"

def call_translation_api(text, target_lang, model_name, reference_text):
    if not text.strip():
        return "Veuillez entrer un texte.", 0.0, "", 0.0, 0.0, 0.0
    
    payload = {
        "text": text,
        "target_lang": target_lang,
        "model": model_name,
        "reference": reference_text
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            metrics = data["metrics"]
            return (
                data["translated_text"],
                data["similarity_score"],
                data["verdict"],
                metrics["bleu"],
                metrics["rouge1"],
                metrics["rougeL"]
            )
        else:
            error = response.json().get('detail', 'Erreur interne')
            return f"Erreur: {error}", 0.0, "Échec", 0.0, 0.0, 0.0
    except requests.exceptions.ConnectionError:
        return "Erreur : Lancez d'abord l'API (api.py).", 0.0, "Déconnecté", 0.0, 0.0, 0.0

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌐 Traducteur augmenté & Évaluation de Métriques")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="Texte source (anglais)", 
                value="Artificial intelligence is transforming the landscape of modern education.", 
                lines=3
            )
            reference_text = gr.Textbox(
                label="Traduction humaine de référence (Optionnel pour BLEU/ROUGE)", 
                value="L'intelligence artificielle transforme le paysage de l'éducation moderne.", 
                lines=2
            )
            
            with gr.Row():
                lang_input = gr.Textbox(label="Langue cible", value="French")
                model_dropdown = gr.Dropdown(label="Modèle Ollama", choices=["llama3", "mistral"], value="llama3", allow_custom_value=True)
                
            submit_btn = gr.Button("Traduire et Calculer les Métriques", variant="primary")
            
        with gr.Column():
            output_text = gr.Textbox(label="Traduction générée par l'IA", interactive=False, lines=3)
            
            gr.Markdown("### 📊 Scores de performance")
            with gr.Row():
                output_score = gr.Number(label="Similarité Cosinus", precision=4)
                output_verdict = gr.Textbox(label="Verdict Sémantique")
                
            with gr.Row():
                output_bleu = gr.Number(label="Score BLEU", precision=4)
                output_rouge1 = gr.Number(label="ROUGE-1 (Mots)", precision=4)
                output_rougel = gr.Number(label="ROUGE-L (Structure)", precision=4)

    submit_btn.click(
        fn=call_translation_api,
        inputs=[input_text, lang_input, model_dropdown, reference_text],
        outputs=[output_text, output_score, output_verdict, output_bleu, output_rouge1, output_rougel]
    )

if __name__ == "__main__":
    demo.launch()