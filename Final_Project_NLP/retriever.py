from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from huggingface_hub import InferenceClient
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

    prompt_template = """Contexte : {context}

Question : {question}

Réponds en français en utilisant uniquement le contexte ci-dessus. Si la réponse est introuvable, dis-le."""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )

    client = InferenceClient(
        token=config.HF_TOKEN,
    )

    def call_llm(prompt_value):
        prompt_text = prompt_value.text if hasattr(prompt_value, "text") else str(prompt_value)

        result = client.post(
            model=config.LLM_REPO_ID,
            json={
                "inputs": prompt_text,
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.2
                }
            }
        )
        
        import json
        try:
            res_json = json.loads(result.decode("utf-8"))
            if isinstance(res_json, list) and len(res_json) > 0:
                return res_json[0].get("generated_text", str(res_json))
            return str(res_json)
        except Exception:
            return result.decode("utf-8")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | RunnableLambda(call_llm)
        | StrOutputParser()
    )

    return rag_chain