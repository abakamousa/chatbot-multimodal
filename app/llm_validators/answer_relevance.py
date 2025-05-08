from .base import Validator

class AnswerRelevanceValidator(Validator):
    """Simple check for empty or irrelevant answers."""

    def validate(self, text: str) -> dict:
        if not text or len(text.strip()) < 5:
            return {"valid": False, "reason": "Answer is too short or empty."}

        if "I'm not sure" in text or "As an AI language model" in text:
            return {"valid": False, "reason": "Answer may be vague or irrelevant."}

        return {"valid": True}
