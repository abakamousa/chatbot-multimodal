import os
import base64
import fitz  # PyMuPDF
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from app.services.azure_openai import AzureOpenAIWrapper
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
import torch
import io
import asyncio

# Load LLaVA-1.5 model and processor once (global, outside the function for efficiency)
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf").to("cuda" if torch.cuda.is_available() else "cpu")

async def caption_image(image_bytes: bytes) -> str:
    """
    Generate a caption for an image using LLaVA-1.5 model.
    :param image_bytes: The image in bytes.
    :return: Caption string.
    """
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    prompt = "Describe this image in one sentence."

    inputs = processor(prompt, image, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=60)
    caption = processor.decode(output[0], skip_special_tokens=True)
    # LLaVA returns the prompt + answer, so remove the prompt
    if caption.lower().startswith(prompt.lower()):
        caption = caption[len(prompt):].strip()
    return caption.strip()

# --- Main async indexing logic ---
async def main():
    openai_client = AzureOpenAIWrapper()
    embedding_model = openai_client.get_embedding_function()

    # Define base directories for PDFs and FAISS index storage
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pdf_directory = os.path.join(BASE_DIR, "data", "docs")
    faiss_index_directory = os.path.join(BASE_DIR, "data", "faiss_index")

    # Load and split PDFs (text)
    documents = []
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            # Load text
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

            # --- Extract images and caption them ---
            doc = fitz.open(pdf_path)
            for page_num, page in enumerate(doc):
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    caption = await caption_image(image_bytes)
                    # Add the caption as a document chunk
                    documents.append(
                        Document(
                            page_content=f"[Image on page {page_num+1} of {filename}]: {caption}",
                            metadata={"source": filename, "page": page_num+1, "type": "image"}
                        )
                    )

    # Split documents into chunks for embedding and retrieval
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    # Create FAISS index
    faiss_index = FAISS.from_documents(split_docs, embedding_model)

    # Save index with metadata
    os.makedirs(faiss_index_directory, exist_ok=True)
    faiss_index.save_local(faiss_index_directory)

    print("✅ FAISS index with image captions created and saved successfully!")

if __name__ == "__main__":
    asyncio.run(main())