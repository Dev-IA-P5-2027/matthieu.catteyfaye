import os
import torch
import requests
from pypdf import PdfReader
import chromadb
import spacy
from sentence_transformers import SentenceTransformer

class RAGEngine:
    def __init__(self, directory_path="data_business"):
        print("Initialisation du RAG Engine...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Utilisation du périphérique : {self.device}")

        # Chargement de spaCy pour un découpage propre par phrases
        print("Chargement de spaCy (en_core_web_sm)...")
        self.nlp = spacy.load("en_core_web_sm")

        # 1. Initialisation de ChromaDB
        self.chroma_client = chromadb.Client()
        self.collection_name = "pdf_documents"
        
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.chroma_client.create_collection(name=self.collection_name)
        
        # 2. Chargement du modèle d'embedding (Hugging Face)
        print("Chargement du modèle d'embedding (all-mpnet-base-v2)...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device=self.device)
        
        # 3. Configuration du modèle de génération via Ollama (local)
        # Pré-requis : avoir Ollama installé et lancé (ollama serve), et le modèle déjà
        # téléchargé une fois avec : ollama pull llama3
        self.ollama_url = "http://localhost:11434/api/generate"
        self.ollama_model = "llama3"
        print(f"Génération configurée pour utiliser Ollama (modèle : {self.ollama_model})...")
        self._check_ollama()
        
        # 4. Indexation AUTOMATIQUE du dossier data_business au démarrage
        print(f"Indexation automatique des fichiers du dossier : '{directory_path}'...")
        self.index_directory(directory_path)
        print("RAG Engine prêt et base vectorielle alimentée !")

    def _check_ollama(self):
        """Vérifie qu'Ollama tourne et que le modèle est disponible, sans bloquer le démarrage."""
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=3)
            resp.raise_for_status()
            available = [m["name"] for m in resp.json().get("models", [])]
            if not any(self.ollama_model in name for name in available):
                print(
                    f"⚠️  Attention : le modèle '{self.ollama_model}' ne semble pas installé dans Ollama. "
                    f"Lancez : ollama pull {self.ollama_model}"
                )
            else:
                print(f"✅ Ollama détecté, modèle '{self.ollama_model}' disponible.")
        except requests.exceptions.RequestException:
            print(
                "⚠️  Attention : impossible de contacter Ollama sur http://localhost:11434. "
                "Vérifiez qu'Ollama est lancé (commande : ollama serve)."
            )

    def pdf_to_text(self, pdf_path):
        """Extrait le texte d'un PDF page par page."""
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n\n"
        return text

    def chunk_text(self, text, max_chars=1000):
        """Découpe le texte en morceaux basés sur les phrases de spaCy (Évite les coupures brutes)."""
        doc = self.nlp(text)
        chunks = []
        current_chunk = ""
        for sent in doc.sents:
            if len(current_chunk) + len(sent.text) > max_chars:
                chunks.append(current_chunk.strip())
                current_chunk = sent.text
            else:
                current_chunk += " " + sent.text
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    def index_directory(self, directory):
        """Parcourt le dossier, extrait, découpe et injecte dans ChromaDB."""
        if not os.path.exists(directory):
            print(f"Attention : Le dossier '{directory}' n'existe pas.")
            return

        all_chunks = []
        all_ids = []
        all_metadatas = []

        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                path = os.path.join(directory, filename)
                print(f"Extraction et découpage de : {filename}...")
                text = self.pdf_to_text(path)
                chunks = self.chunk_text(text)
                
                for index, chunk in enumerate(chunks):
                    # Génération d'un ID unique similaire à votre exemple
                    doc_id = f"{filename}:part{index+1}"
                    all_chunks.append(chunk)
                    all_ids.append(doc_id)
                    all_metadatas.append({"source": filename, "chunk_id": index})

        # Injection par lot (Batch) dans ChromaDB si des fragments ont été trouvés
        if all_chunks:
            print(f"Calcul des embeddings et stockage de {len(all_chunks)} fragments...")
            embeddings = self.embedding_model.encode(all_chunks).tolist()
            self.collection.add(
                ids=all_ids,
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadatas
            )
            print(f"Succès : {len(all_chunks)} fragments ajoutés à la base vectorielle.")

    def answer_question(self, question: str, n_results: int = 3) -> tuple:
        """Recherche les documents pertinents et génère la réponse."""
        if not question.strip():
            return "Veuillez poser une question valide.", ""

        query_embedding = self.embedding_model.encode(question).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        retrieved_docs = results['documents'][0] if results['documents'] else []
        retrieved_ids = results['ids'][0] if results['ids'] else []
        
        if not retrieved_docs:
            return "Aucun contexte trouvé pour répondre à cette question.", ""

        context = "\n---\n".join(retrieved_docs)
        
        # Consigne stricte en anglais (mieux comprise par Flan-T5) pour forcer une réponse en français
        prompt = (
            f"Instruction: Answer the question in English based only on the provided context. "
            f"If the answer cannot be found in the context, say 'I don't know'.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            f"Answer (in English):"
        )
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1},
                },
                timeout=120,
            )
            response.raise_for_status()
            response_text = response.json().get("response", "").strip()
        except requests.exceptions.RequestException as e:
            response_text = (
                "Erreur : impossible de contacter Ollama (vérifiez que 'ollama serve' "
                f"tourne et que le modèle '{self.ollama_model}' est installé). Détail : {e}"
            )
        
        sources = "\n".join([f"- {doc_id}" for doc_id in retrieved_ids])
        
        return response_text, sources