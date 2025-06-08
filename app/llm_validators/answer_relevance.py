# app/llm_validators/answer_relevance.py

from app.llm_validators.base import Validator
from app.services.azure_openai import AzureOpenAIWrapper
from app.utils.helpers import get_logger

logger = get_logger(__name__)

class AnswerRelevanceValidator(Validator):
    def __init__(self, openai_service: AzureOpenAIWrapper):
        self.openai_service = openai_service

    async def validate(self, question: str, answer: str) -> bool:
        """Validates whether the given answer is relevant to the question."""
        prompt = (
            "You are a helpful assistant evaluating the relevance of answers given to user questions.\n\n"
            "Evaluate whether the following answer correctly and directly addresses the user's question.\n\n"
            "If the answer is relevant, respond with 'YES'. If it is not relevant, respond with 'NO'.\n\n"
            f"Question:\n\"{question}\"\n\n"
            f"Answer:\n\"{answer}\""
        )

        try:
            messages = [
                {"role": "user", "content": prompt}
            ]
            response = await self.openai_service.chat_completion(messages)
            

            logger.info(f"Answer Relevance Validator response: {response}")
            return response

        except Exception as e:
            logger.error(f"Error during answer relevance validation: {e}")
            return False  # Treat as irrelevant if evaluation fails
