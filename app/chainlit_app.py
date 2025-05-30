# app/chainlit_app.py

import chainlit as cl
from app.services.azure_openai import AzureOpenAIWrapper
from app.llm_validators.prompt_injection import PromptInjectionValidator
from app.llm_validators.answer_relevance import AnswerRelevanceValidator
from app.utils.helpers import get_logger
from app.config.settings import get_settings
from app.chains.langchain_rag import chat_with_rag





settings = get_settings()
logger = get_logger(__name__)

# Initialize AzureOpenAIWrapper
openai_service = AzureOpenAIWrapper()

# Initialize the Validators
prompt_injection_validator = PromptInjectionValidator(openai_service=openai_service)
answer_relevance_validator = AnswerRelevanceValidator(openai_service=openai_service)



@cl.on_message
async def on_message(message: str):
    """This function handles the incoming messages and performs validation checks."""
    logger.info(f"Received message: {message}")

    # 1. Validate prompt injection
    if await prompt_injection_validator.validate(message)== "YES":
        logger.warning("Potential prompt injection detected.")
        await cl.Message(content="Potential prompt injection detected. Please rephrase your request.").send()
        return

    # 2. Generate a response from the model using Azure OpenAI
    try:
        user_query = message.content
        # Generate response
        response = chat_with_rag(user_query)
        #response = await openai_service.chat_completion(user_query)
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        await cl.Message(content="Sorry, something went wrong while processing your request.").send()
        return

    # 3. Validate answer relevance (optional - this is an additional step to make sure the response is valid)
    if await answer_relevance_validator.validate(message, response) == "YES":
        await cl.Message(content="The response seems irrelevant to your query. Please try again.").send()
        return

    # 4. Send the response back to the user
    await cl.Message(content=response).send()


@cl.on_chat_start
async def on_chat_start():
    """This function handles the initialization when the chat starts."""
    await cl.Message(content="Hello! How can I assist you today?").send()
