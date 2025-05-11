# Chatbot Multimodal Application



## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Setup Instructions](#2-setup-instructions)
  - [3. Running the Application](#3-running-the-application)
  - [4. Running the Azure Function](#4-running-the-azure-function)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [License](#license)
- [Author](#author)



## 📘 Project Overview

**Chatbot Multimodal** is an intelligent, Azure-powered RAG (Retrieval-Augmented Generation) system built to handle both text and image-based queries. It leverages enterprise-grade capabilities like **Azure OpenAI**, **FAISS vector search**, and **LangChain** to provide accurate, context-aware responses based on a knowledge base of PDF documents and optional image inputs. It includes additional features like **Prompt Injection Validation** and **Answer Relevance Validation** to ensure high-quality and relevant responses.

### 💡 Key Features

- **Document Intelligence**  
  Ingests and processes PDFs using LangChain and PDFMiner.

- **RAG Pipeline**  
  Combines document retrieval with Azure OpenAI’s large language model for informed, contextual answers.

- **Vector Store with FAISS**  
  Embeds and indexes documents for efficient semantic search.

- **Image Captioning (Optional)**  
  Enhances responses by generating and incorporating captions for user-provided images.

- **Modern Chat Interface**  
  Interact through a Chainlit-powered chat UI for a seamless user experience.

- **Serverless API Integration**  
  Deployable via Azure Functions for scalable and cloud-native access.



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
This will automatically install the dependencies defined in your pyproject.toml file.

e) **Set up environment variables**:

```ini
# Azure OpenAI Settings
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
api_version=2024-12-01-preview
```
### Running the Application 

To start the application locally, run: 
```bash
 chainlit run app/chainlit_app.py -w
```
Your application will be available at http://127.0.0.1:8000.

### ⚡ Running the Azure Function

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

Once the application is running, you can interact with the chatbot via the provided chat interface. The chatbot utilizes Azure OpenAI for generating responses, while validating both inputs and outputs to ensure security and relevance.

## Project Structure

Here's an overview of the project directory structure:

```bash
 chatbot-multimodal/
├── app/
│   ├── __init__.py
│   ├── main.py                 # main Chainlit app for running the chatbot
│   ├── chainlit_app.py         # Chainlit app for running the chatbot
│   ├── data/
│   │   ├──faiss_index 
│   │   └──docs
│   ├── services/
│   │   └── azure_openai.py     # Azure OpenAI wrapper for API calls
│   ├── llm_validators/
│   │   ├── __init__.py
│   │   ├── base.py             # Base validator class
│   │   ├── prompt_injection.py # Prompt injection validation logic
│   │   └── answer_relevance.py # Answer relevance validation logic
│   ├── utils/
│   │   └── helpers.py          # Helper functions, including logging setup
│   ├── config/
│   │   └── settings.py         # Configuration settings (Pydantic)
├── azure_functions/            # Directory for Azure Function-related code
│   ├── __init__.py             # Azure function initialization
│   ├── function_handler.py     # Logic for handling Azure Functions (e.g., HTTP triggers)
│   └── function_config.py      # Azure function configuration settings (if needed)
├── .env                        # Environment variables (API keys, etc.)
├── pyproject.toml              # Project metadata and dependencies (using UV)
└── README.md                   # This README file


```
## 🧯 Troubleshooting

  - FAISS load errors: Ensure index is created and located at app/data/faiss_index.

  -  Module import issues: Add the project root to PYTHONPATH.

  - Python 3.13 not supported: Downgrade to Python 3.12.x.

## License

xxx

## Author



- **ABOUBAKAR Moussa** – AI Engineer &rarr; [GitHub](https://github.com/abakamousa/) · [LinkedIn](https://www.linkedin.com/in/aboubakar-moussa/)

