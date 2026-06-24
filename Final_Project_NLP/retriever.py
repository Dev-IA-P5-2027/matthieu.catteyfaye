# retriever.py
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import config

def format_docs(docs):
    """Combine les textes des documents récupérés en une seule chaîne."""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        path=config.QDRANT_PATH,
        collection_name=config.COLLECTION_NAME
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = HuggingFaceEndpoint(
        repo_id=config.LLM_REPO_ID,
        huggingfacehub_api_token=config.HF_TOKEN,
        temperature=0.2,
        max_new_tokens=512
    )

    system_prompt = (
        "Tu es un assistant expert. Réponds à la question en utilisant uniquement le contexte fourni ci-dessous. "
        "Si tu ne connais pas la réponse, dis simplement que tu ne sais pas.\n\n"
        "Contexte :\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain