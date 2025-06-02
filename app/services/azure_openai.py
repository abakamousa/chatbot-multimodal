# app/services/azure_openai.py
from openai import AzureOpenAI
#from azure.core.credentials import AzureKeyCredential
from typing import List, Optional
import logging
import os
from app.utils.helpers import get_logger
from langchain.embeddings.base import Embeddings
from app.config.settings import get_settings

logger = get_logger(__name__)


class AzureOpenAIWrapper:
    def __init__(self):
        settings = get_settings()

        self.api_key = settings.azure_openai_api_key
        self.endpoint = settings.azure_openai_endpoint
        self.deployment_name = settings.azure_openai_deployment_name
        self.embedding_deployment = settings.azure_openai_embedding_deployment
        self.api_version = settings.azure_openai_api_version

        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            #credential=AzureKeyCredential(self.api_key)
        )

        
   
    async def chat_completion(self, user_input: str, temperature: float = 0.2, max_tokens: int = 800) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages= user_input,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content 
        except Exception as e:
            logger.warning("Failed to generate chat completion")
            raise RuntimeError(f"Chat completion error: {str(e)}")

    
    def get_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                input=[text],
                model=self.embedding_deployment
            )
            return response.data[0].embedding
        except Exception as e:
            logger.exception("Failed to generate embedding")
            raise RuntimeError(f"Embedding error: {str(e)}")
    
    def get_embedding_function(self) -> Embeddings:
        """
        Returns an object compatible with LangChain embedding APIs.
        """
        class AzureEmbeddingWrapper(Embeddings):
            def __init__(self, client):
                self.client = client

            def embed_documents(self, texts: List[str]) -> List[List[float]]:
                return [self.client.get_embedding(text) for text in texts]

            def embed_query(self, text: str) -> List[float]:
                return self.client.get_embedding(text)

        return AzureEmbeddingWrapper(self)
