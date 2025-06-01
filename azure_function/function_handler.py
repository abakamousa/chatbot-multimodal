import azure.functions as func
import json
import tempfile
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

        user_input = None
        image_path = None

        # Handle multipart/form-data (with image)
        
        content_type = req.headers.get("Content-Type", "")
        if content_type.startswith("multipart/form-data"):
            form = req.form  # <-- No parentheses
            user_input = form.get("message")
            image_file = form.get("image")
            if image_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(image_file.read())
                    image_path = tmp.name
        else:
            # Handle application/json
            req_body = req.get_json()
            user_input = req_body.get("message")

        if not user_input:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'message' in request body."}),
                status_code=400,
                mimetype="application/json"
            )

        logger.info(f"Received message: {user_input}")

        # Prompt injection validation (if enabled)
        if settings.function_enable_prompt_validation:
            logger.info("Prompt injection validation is enabled.")
            is_prompt_injection = await prompt_validator.validate(user_input)
            if is_prompt_injection == "YES":
                logger.warning("Prompt injection detected.")
                return func.HttpResponse(
                    json.dumps({"error": "Prompt injection attempt detected."}),
                    status_code=400,
                    mimetype="application/json"
                )

        # Generate response (pass image_path if present)
        response = chat_with_rag(user_input, image_path=image_path)

        # Answer relevance validation (if enabled)
        if settings.function_enable_relevance_validation:
            logger.info("Answer relevance validation is enabled.")
            is_relevant = await relevance_validator.validate(user_input, response)
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