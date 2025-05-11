from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from app.services.azure_openai import AzureOpenAIWrapper
import os

openai_client = AzureOpenAIWrapper()
embedding_model = openai_client.get_embedding_function()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_directory = os.path.join(BASE_DIR, "data", "docs")
faiss_index_directory = os.path.join(BASE_DIR, "data", "faiss_index")

# Load and split PDFs
documents = []
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_directory, filename))
        documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(documents)

# Create FAISS index
faiss_index = FAISS.from_documents(split_docs, embedding_model)

# Save index with metadata
os.makedirs(faiss_index_directory, exist_ok=True)
faiss_index.save_local(faiss_index_directory)


print("✅ FAISS index created and saved successfully!")
