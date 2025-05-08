import re
from app.llm_validators.base import Validator

class PromptInjectionValidator(Validator):
    """Detects potential prompt injection in user inputs."""

    def validate(self, text: str) -> dict:
        injection_patterns = [
            r"(?i)forget previous instructions",
            r"(?i)you are now",
            r"(?i)ignore.*(previous|above) instructions",
            r"(?i)pretend to be",
            r"(?i)act as",
            r"(?i)system:",
        ]
        for pattern in injection_patterns:
            if re.search(pattern, text):
                return {
                    "valid": False,
                    "reason": f"Possible prompt injection detected: `{pattern}`"
                }
        return {"valid": True}
