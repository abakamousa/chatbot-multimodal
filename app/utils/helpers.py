import logging
import json
import base64
import io
from typing import Any, Dict, List, Union, Optional

from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# --- Basic Chat Helpers ---

def format_chat_messages(user_message: str, system_prompt: str = None) -> List[Dict[str, str]]:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})
    return messages

def safe_json_parse(data: Union[str, bytes]) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except Exception as e:
        logger.warning(f"JSON parsing failed: {e}")
        return {}

def truncate_text(text: str, max_tokens: int = 1000) -> str:
    words = text.split()
    return " ".join(words[:max_tokens])

def redact_sensitive_keys(d: Dict[str, Any], keys: List[str] = ["api_key", "password", "token"]) -> Dict[str, Any]:
    return {k: "[REDACTED]" if k.lower() in keys else v for k, v in d.items()}


# --- Image Helpers ---

def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Converts a PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def preprocess_image(file_path: str, size: Optional[tuple] = (512, 512)) -> str:
    """Loads, resizes, and encodes an image to base64."""
    try:
        image = Image.open(file_path).convert("RGB")
        if size:
            image = image.resize(size)
        return image_to_base64(image)
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise


# --- (Optional) Azure Text-to-Speech ---

def synthesize_speech(text: str, voice: str = "en-US-JennyNeural") -> bytes:
    """
    Requires: azure-cognitiveservices-speech
    """
    try:
        import azure.cognitiveservices.speech as speechsdk
        from app.config.settings import get_settings

        settings = get_settings()

        speech_config = speechsdk.SpeechConfig(
            subscription=settings.azure_tts_key,
            region=settings.azure_tts_region
        )
        speech_config.speech_synthesis_voice_name = voice

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        else:
            logger.error(f"TTS failed: {result.reason}")
            raise RuntimeError("Speech synthesis failed.")
    except ImportError:
        raise ImportError("Please install 'azure-cognitiveservices-speech' for TTS support.")

