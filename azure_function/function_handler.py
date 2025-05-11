import azure.functions as func
import json
from app.services.azure_openai import AzureOpenAIWrapper
from app.llm_validators.prompt_injection import PromptInjectionValidator
from app.llm_validators.answer_relevance import AnswerRelevanceValidator
from app.utils.helpers import get_logger
from app.chains.langchain_rag import chat_with_rag
from azure_function.function_config import get_function_settings

logger = get_logger(__name__)

settings = get_function_settings()

if settings.function_enable_logging:
    logger.info("Azure Function config loaded.")



azure_service = AzureOpenAIWrapper()
prompt_validator = PromptInjectionValidator(azure_service)
relevance_validator = AnswerRelevanceValidator(azure_service)

async def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logger.info("Azure Function triggered")

        req_body = req.get_json()
        user_input = req_body.get("message")

        if not user_input:
            return func.HttpResponse("Missing 'message' in request body.", status_code=400)

        logger.info(f"Received message: {user_input}")

        # Run prompt injection check
        is_prompt_injection =  prompt_validator.validate(user_input)
        if is_prompt_injection == "YES":
            logger.warning("Prompt injection detected.")
            return func.HttpResponse(
                json.dumps({"error": "Prompt injection attempt detected."}),
                status_code=400,
                mimetype="application/json"
            )
        # Generate response
        #response = await azure_service.chat_completion(user_input)
        # Call the chat_with_agent function from langchain_agent.py to get a response
        response = chat_with_rag(user_input)
        # Run answer relevance check (optional)
        is_relevant = relevance_validator.validate(user_input, response)
        if is_relevant == "NO":
            logger.warning("Input deemed not relevant.")
            return func.HttpResponse(
                json.dumps({"error": "Input does not seem relevant to the expected context."}),
                status_code=400,
                mimetype="application/json"
            )

       

        return func.HttpResponse(
            json.dumps({"response": response}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logger.exception("Error in Azure Function handler")
        return func.HttpResponse(
            json.dumps({"error": f"Internal Server Error: {str(e)}"}),
            status_code=500,
            mimetype="application/json"
        )
