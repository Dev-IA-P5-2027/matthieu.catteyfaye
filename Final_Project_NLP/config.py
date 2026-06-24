import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()

        self.HF_TOKEN = os.getenv("HF_TOKEN")
        self.EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
        self.LLM_REPO_ID = "google/flan-t5-large"
        self.QDRANT_PATH = "./qdrant_db"
        self.COLLECTION_NAME = "my_pdf_documents"


config = Settings()