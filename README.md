# Chatbot Multimodal Application

A robust, Azure-powered Retrieval-Augmented Generation (RAG) chatbot that supports both text and image-based queries. Built with LangChain, FAISS, Azure OpenAI, and Chainlit for a modern, multimodal conversational experience.


## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Setup Instructions](#2-setup-instructions)
  - [3. Creating the FAISS Index](#3-creating-the-faiss-index)
  - [4. Running the Application](#4-running-the-application)
  - [5. Running the Azure Function](#5-running-the-azure-function)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [License](#license)
- [Author](#author)



## 📘 Project Overview

**Chatbot Multimodal** is an intelligent, enterprise-ready chatbot that leverages:
- **Azure OpenAI** for advanced language understanding,
- **FAISS** for fast semantic search over your documents,
- **LangChain** for RAG pipelines,
- **Chainlit** for a modern chat UI.

It supports both text and image queries, and includes prompt injection and answer relevance validation for security and quality.


### 💡 Key Features

- **Document Intelligence:** Ingests and processes PDFs for knowledge retrieval.
- **RAG Pipeline:** Combines document retrieval with Azure OpenAI for contextual answers.
- **Vector Store with FAISS:** Efficient semantic search over your knowledge base.
- **Image Captioning (Optional):** Enhances responses with image understanding.
- **Modern Chat Interface:** Built with Chainlit for a seamless user experience.
- **Serverless API:** Deployable via Azure Functions for scalable, cloud-native access.
- **Security:** Prompt injection and answer relevance validation.


## 🧰 Technologies Used

### ⚙️ Core Technologies
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Azure Functions](https://img.shields.io/badge/Azure%20Functions-Serverless-blue?logo=microsoft-azure)
![uv](https://img.shields.io/badge/uv-package--manager-4B8BBE)

### 🤖 AI & Embeddings
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--powered-blue?logo=openai)
![LangChain](https://img.shields.io/badge/LangChain-RAG-yellowgreen?logo=python)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-green)

### 📄 Document Handling
![PDFMiner](https://img.shields.io/badge/pdfminer--six-PDF%20Parsing-lightgrey)
![LangChain Loader](https://img.shields.io/badge/LangChain%20Loaders-Document%20Utils-blueviolet)
![Text Splitter](https://img.shields.io/badge/Text%20Splitter-Chunking-yellow)

### 🖼️ Image & Multimodal
![Image Captioning](https://img.shields.io/badge/Image%20Captioning-Optional-orange)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-lightblue)

### 🌐 Web & UI
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20Framework-teal?logo=fastapi)
![Chainlit](https://img.shields.io/badge/Chainlit-Chat%20UI-orange)

### 🔧 Tooling
![Pydantic](https://img.shields.io/badge/Pydantic-Settings%20Validation-brightgreen)
![dotenv](https://img.shields.io/badge/python--dotenv-.env%20Support-blue)
![Black](https://img.shields.io/badge/black-code%20formatter-black)
![Ruff](https://img.shields.io/badge/ruff-linter-orange)


## Setup

### 1. Prerequisites

Before setting up the project, ensure you have the following:

- **Python 3.8+**
- **Azure OpenAI Account** (for API keys and configuration)
- **Visual Studio Code** or any text editor/IDE of your choice

### 2. Setup Instructions

a) **Clone the repository**:

```bash
git clone https://github.com/your-username/chatbot-multimodal.git
cd chatbot-multimodal
```
b) **Create a virtual environment**:
```bash
uv  venv 
```
c) **Activate the virtual environment**:
Windows (PowerShell):
```bash
.\venv\Scripts\Activate
```
d) **Install required dependencies using uv**:

```bash
uv sync
```
This will automatically install all the dependencies from `pyproject.toml`

e) **Set up environment variables**:

```ini
# Azure OpenAI Settings (Production)
AZURE_OPENAI_API_KEY=your-production-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-production-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Azure Function Settings
FUNCTION_ENVIRONMENT=production
FUNCTION_ENABLE_LOGGING=True
FUNCTION_ENABLE_PROMPT_VALIDATION=True
FUNCTION_ENABLE_RELEVANCE_VALIDATION=True

# App Insights (real key)
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

```
f) **Create the FAISS index**

Before running the chatbot, you **must** create the FAISS vector index from your PDF documents. This step is required for semantic search to work.

From the project root, run:

```bash
python -m app.chains.create_faiss_index
```

This will process all PDF files in `app/data/docs/` and generate the FAISS index files in `app/data/faiss_index/`.  
If you add or update documents, re-run this command to refresh the index.
### 4. Running the Application 

To start the Chainlit chat UI  locally, run: 
```bash
 chainlit run app/chainlit_app.py -w
```
Your application will be available at http://127.0.0.1:8000.

### ⚡ 5. Running the Azure Function

a) **Start azure function**:
To test the RAG chatbot as an Azure Function, install Azure Functions Core Tools and run: 
```bash
 func start
```

b) **start chainlit app**:
To start the application using azure function, run: 

```bash
 chainlit run app/main.py -w
```


## Usage

Once running, interact with the chatbot via the Chainlit UI.  
- The chatbot uses Azure OpenAI for responses.
- All inputs and outputs are validated for security and relevance.


## 🧯 ## Troubleshooting

- **FAISS load errors:**  
  Ensure the index is created and located at `app/data/faiss_index/`.

- **Module import issues:**  
  Run all commands from the project root, or set `PYTHONPATH` to the project root.

- **Python 3.13 not supported:**  
  Use Python 3.12.x.

- **Azure Function not loading:**  
  Check `function.json` and ensure all dependencies are installed.

- **ModuleNotFoundError: No module named 'app':**  
  Run scripts as modules from the project root, e.g.,  
  `python -m app.chains.create_faiss_index`

---

## Project Structure

```bash
chatbot-multimodal/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Chainlit app for Azure Function backend
│   ├── chainlit_app.py         # Main Chainlit chat UI
│   ├── data/
│   │   ├── faiss_index         # FAISS vector index files
│   │   └── docs                # PDF documents
│   ├── services/
│   │   └── azure_openai.py     # Azure OpenAI wrapper
│   ├── llm_validators/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── prompt_injection.py
│   │   └── answer_relevance.py
│   ├── utils/
│   │   └── helpers.py
│   ├── config/
│   │   └── settings.py
│   └── chains/
│       ├── langchain_rag.py
│       └── create_faiss_index.py
├── azure_functions/
│   ├── __init__.py
│   ├── function_handler.py
│   └── function_config.py
├── .env
├── pyproject.toml
└── README.md
```


## License

xxx

## Author



- **ABOUBAKAR Moussa** – AI Engineer &rarr; [GitHub](https://github.com/abakamousa/) · [LinkedIn](https://www.linkedin.com/in/aboubakar-moussa/)

