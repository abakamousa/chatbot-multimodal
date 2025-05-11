# app/utils/build_faiss_index.py

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader, UnstructuredPDFLoader
from app.config.settings import get_settings

# Get app settings
settings = get_settings()

# Initialize the embedding model
embedding_model = OpenAIEmbeddings(
    deployment=settings.azure_openai_embedding_deployment,
    openai_api_key=settings.azure_openai_api_key,
    openai_api_base=settings.azure_openai_endpoint,
    openai_api_version=settings.azure_openai_api_version,
    openai_api_type="azure"
)

def load_documents(directory: str):
    """Load documents from the specified directory."""
    loaders = [
        TextLoader,
        UnstructuredPDFLoader
    ]
    docs = []
    for loader_cls in loaders:
        loader = DirectoryLoader(directory, loader_cls=loader_cls)
        docs.extend(loader.load())
    return docs

def build_faiss_index():
    """Load documents, create FAISS index, and save it locally."""
    doc_path = "data/docs"  # Directory where docs are located
    documents = load_documents(doc_path)

    if not documents:
        raise ValueError("No documents found in the directory.")

    print(f"Loaded {len(documents)} documents.")

    # Create FAISS index from documents
    db = FAISS.from_documents(documents, embedding_model)

    # Save the FAISS index to the specified directory
    index_path = "data/faiss_index"
    db.save_local(index_path)
    print(f"✅ FAISS index built and saved to '{index_path}'")

if __name__ == "__main__":
    build_faiss_index()
    