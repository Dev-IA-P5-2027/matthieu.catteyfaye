import os
import torch
from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForText2TextGeneration, pipeline

class RAGEngine:
    def __init__(self):
        print("Initialisation du RAG Engine...")
        # 1. Initialisation du client de base de données vectorielle locale
        self.chroma_client = chromadb.Client()
        self.collection_name = "pdf_documents"
        
        # Supprime la collection si elle existe déjà pour éviter les mélanges
        try:
            self.chroma_client.delete_collection(name=self.collection_name)
        except Exception:
            pass
        self.collection = self.chroma_client.create_collection(name=self.collection_name)
        
        # 2. Chargement du modèle d'embedding imposé par l'énoncé
        print("Chargement du modèle d'embedding (all-mpnet-base-v2)...")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        
        # 3. Chargement du modèle de génération imposé par l'énoncé
        print("Chargement du modèle de génération (flan-t5-large)...")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
        self.llm_model = AutoModelForText2TextGeneration.from_pretrained("google/flan-t5-large")
        
        # Création du pipeline de génération de texte
        self.generation_pipeline = pipeline(
            "text2text-generation",
            model=self.llm_model,
            tokenizer=self.tokenizer,
            max_length=256,
            temperature=0.2,
            do_sample=True
        )
        print("RAG Engine prêt !")

    def process_pdf(self, pdf_path: str, chunk_size: int = 800, overlap: int = 150):
        """Extrait le texte d'un PDF, le découpe en morceaux et le stocke dans ChromaDB."""
        if not pdf_path:
            return "Aucun fichier fourni."
        
        print(f"Traitement du fichier : {pdf_path}")
        reader = PdfReader(pdf_path)
        full_text = ""
        
        # Extraction du texte page par page
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        if not full_text.strip():
            return "Le PDF semble vide ou illisible."

        # Découpage du texte en morceaux (Chunking avec overlap)
        chunks = []
        words = full_text.split()
        
        # Conversion du découpage en caractères approximatifs pour correspondre au chunk_size
        step = chunk_size - overlap
        for i in range(0, len(full_text), step):
            chunk = full_text[i:i + chunk_size]
            if len(chunk.strip()) > 10:  # Éviter les morceaux vides
                chunks.append(chunk.strip())

        filename = os.path.basename(pdf_path)
        print(f"Génération de {len(chunks)} fragments pour {filename}...")

        # Génération des vecteurs d'embeddings et stockage
        for idx, chunk in enumerate(chunks):
            # Calcul de l'embedding du fragment
            embedding = self.embedding_model.encode(chunk).tolist()
            
            # Ajout à la base ChromaDB
            self.collection.add(
                ids=[f"{filename}_chunk_{idx}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": filename, "chunk_id": idx}]
            )
            
        return f"Succès : Le document '{filename}' a été indexé ({len(chunks)} fragments créés)."

    def answer_question(self, question: str, n_results: int = 3) -> tuple:
        """Recherche les documents pertinents et génère la réponse finale."""
        if not question.strip():
            return "Veuillez poser une question valide.", ""

        # 1. Encoder la question de l'utilisateur
        query_embedding = self.embedding_model.encode(question).tolist()
        
        # 2. Rechercher les morceaux les plus proches dans ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        retrieved_docs = results['documents'][0] if results['documents'] else []
        retrieved_ids = results['ids'][0] if results['ids'] else []
        
        if not retrieved_docs:
            return "Aucun contexte trouvé dans le document. Veuillez d'abord téléverser un PDF.", ""

        # 3. Construire le contexte pour Flan-T5
        context = "\n---\n".join(retrieved_docs)
        
        # Prompt structuré optimisé pour les modèles de type Encoder-Decoder (Flan-T5)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer based only on the context provided above:"
        
        # 4. Générer la réponse
        output = self.generation_pipeline(prompt)
        response_text = output[0]['generated_text']
        
        # Formater les métadonnées de source à afficher dans l'interface
        sources = "\n".join([f"- Fragment extrait : {doc_id}" for doc_id in retrieved_ids])
        
        return response_text, sources