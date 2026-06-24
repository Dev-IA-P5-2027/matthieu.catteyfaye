import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()

        self.HF_TOKEN = os.getenv("HF_TOKEN")
        self.EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
        self.LLM_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3" 
        self.QDRANT_PATH = "./qdrant_db"
        self.COLLECTION_NAME = "my_pdf_documents"


config = Settings()