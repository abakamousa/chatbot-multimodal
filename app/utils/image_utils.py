import base64
import io
from PIL import Image

def preprocess_image(file_path: str, size: tuple = (512, 512)) -> str:
    """Loads, resizes, and encodes an image to base64."""
    try:
        image = Image.open(file_path).convert("RGB")
        if size:
            image = image.resize(size)
        return image_to_base64(image)
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise



def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Converts a PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")