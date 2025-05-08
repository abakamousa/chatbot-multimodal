# Chatbot Multimodal Application

This is a multimodal chatbot application that leverages **Chainlit**, **Langchain**, **Azure OpenAI**, **Uvicorn**, and other technologies to provide a powerful conversational AI experience.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Setup Instructions](#2-setup-instructions)
  - [3. Running the Application](#3-running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

## Overview

This chatbot integrates multiple language models (LLMs) with additional features like **Prompt Injection Validation** and **Answer Relevance Validation** to ensure high-quality and relevant responses. The backend is powered by **Azure OpenAI**, and the app is hosted using **Uvicorn**.

## Features

- **Multimodal Chatbot**: Interact with a chatbot powered by advanced language models.
- **Azure OpenAI Integration**: Securely connect to Azure’s AI services for text generation and analysis.
- **Prompt Injection & Answer Relevance Validation**: Ensures that user inputs and outputs are secure and relevant.
- **Scalable and Fast**: Run locally or deploy to any cloud platform using **Uvicorn** and **Chainlit**.
- **Simple Setup**: Easily deploy and start the application with minimal dependencies.

## Technologies Used

- **Chainlit**: For handling chat interfaces.
- **Langchain**: For chaining different models and processing tasks.
- **Azure OpenAI**: For utilizing OpenAI's models via Azure API.
- **Uvicorn**: ASGI server for fast and asynchronous handling of HTTP requests.
- **Pydantic**: For validating environment variables and application settings.
- **Azure Functions**: For serverless functions (if applicable).

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

## Usage

Once the application is running, you can interact with the chatbot via the provided chat interface. The chatbot utilizes Azure OpenAI for generating responses, while validating both inputs and outputs to ensure security and relevance.

## Project Structure

Here's an updated overview of the project directory structure:

```bash
 chatbot-multimodal/
├── app/
│   ├── __init__.py
│   ├── chainlit_app.py         # Main Chainlit app for running the chatbot
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
## Author



```yaml
Author: 

- **ABOUBAKAR Moussa ** – AI Engineer  
  [GitHub](https://github.com/abakamousa/) · [LinkedIn](https://www.linkedin.com/in/aboubakar-moussa/)

```