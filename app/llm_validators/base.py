from abc import ABC, abstractmethod

class Validator(ABC):
    """Abstract base class for LLM validators."""

    @abstractmethod
    def validate(self, text: str) -> dict:
        """
        Validate input or output text.
        Returns a dict with keys like `valid: bool` and `reason: str`.
        """
        pass
