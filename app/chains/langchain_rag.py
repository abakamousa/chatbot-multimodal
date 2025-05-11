# app/chains/langchain_rag.py

from typing import Optional, List
import os

from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.schema import Document as LCDocument
from langchain.embeddings.base import Embeddings

from app.config.settings import get_settings
from app.services.azure_openai import AzureOpenAIWrapper
from langchain.document_loaders import ImageCaptionLoader
from langchain.chat_models import ChatOpenAI  # or use AzureChatOpenAI if needed

settings = get_settings()
openai_client = AzureOpenAIWrapper()

# Define custom embedding class to wrap AzureOpenAI embeddings
class CustomAzureEmbedding(Embeddings):
    def __init__(self, client: AzureOpenAIWrapper):
        self.client = client

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.client.get_embedding(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.client.get_embedding(text)

# Get absolute path to the FAISS index directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app/chains
APP_DIR = os.path.dirname(BASE_DIR)  # app/
FAISS_INDEX_PATH = os.path.join(APP_DIR, "data", "faiss_index")
if not os.path.exists(os.path.join(FAISS_INDEX_PATH, "index.faiss")):
    raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}. Please run the index creation script.")


# Load FAISS Vector Store
def load_vector_store() -> FAISS:
    embedding_model = CustomAzureEmbedding(openai_client)
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings=embedding_model)



# Setup retriever and QA chain
vector_store = load_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Optionally use AzureChatOpenAI here if you want to use LangChain's abstraction
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        temperature=0,
        openai_api_key=settings.azure_openai_api_key,
        openai_api_base=settings.azure_openai_endpoint,
        openai_api_type="azure",
        openai_api_version=settings.azure_openai_api_version,
        model_name=settings.azure_openai_deployment_name
    ),
    retriever=retriever,
    return_source_documents=True
)

def chat_with_rag(user_input: str, image_path: Optional[str] = None, system_prompt: Optional[str] = None) -> str:
    try:
        # Append image caption if provided
        if image_path:
            loader = ImageCaptionLoader([image_path])
            docs = loader.load()
            image_captions = "\n".join([doc.page_content for doc in docs])
            user_input += f"\n\nImage Content:\n{image_captions}"

        # Compose system prompt if needed (LangChain may not use it directly here)
        final_input = f"{system_prompt or 'You are a helpful assistant.'}\n\n{user_input}"

        result = qa_chain.run(final_input)
        return result

    except Exception as e:
        return f"⚠️ Error during RAG or LLM response: {str(e)}"