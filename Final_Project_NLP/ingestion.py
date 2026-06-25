from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from config import config 


def ingest_docs(docs_dir: str):
    print("Chargement des documents...")
    loader = DirectoryLoader(docs_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    print(f"{len(documents)} pages chargées. Découpage...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    print("Génération des embeddings et stockage LOCAL dans Qdrant...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        path=config.QDRANT_PATH,
        collection_name=config.COLLECTION_NAME
    )
    print(f"Ingestion terminée ! Base stockée dans le dossier : {config.QDRANT_PATH}")

if __name__ == "__main__":
    ingest_docs("data")