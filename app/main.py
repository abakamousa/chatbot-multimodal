import chainlit as cl
import httpx
import os

AZURE_FUNCTION_URL = "http://localhost:7071/api/chatbot" #"https://chatbot-multimodal.azurewebsites.net/"  #"http://localhost:7071/api/chatbot"  #os.getenv("AZURE_FUNCTION_URL")  # e.g., "https://your-func-name.azurewebsites.net/api/chatbot"



@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hello! I'm your assistant. You can send text or attach an image for multimodal answers.").send()

@cl.on_message
async def on_message(message: cl.Message):
    files = message.elements or []
    image_bytes = None
    image_filename = None

    # If an image is attached, read its bytes
    if files:
        file = files[0]
        image_filename = file.name
        with open(file.path, "rb") as f:
            image_bytes = f.read()

    # Prepare the request payload
    data = {"message": message.content}
    files_payload = None

    if image_bytes and image_filename:
        files_payload = {"image": (image_filename, image_bytes, "application/octet-stream")}

    async with httpx.AsyncClient() as client:
        try:
            if files_payload:
                res = await client.post(
                    AZURE_FUNCTION_URL,
                    data=data,
                    files=files_payload,
                    timeout=60
                )
            else:
                res = await client.post(
                    AZURE_FUNCTION_URL,
                    json=data,
                    timeout=30
                )
            res.raise_for_status()
            if res.text:
                data = res.json()
                reply = data.get("response", "No response.")
            else:
                reply = "❌ Error: Empty response from server."
        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get('error', str(e))
            except Exception:
                error_detail = str(e)
            reply = f"❌ Error: {error_detail}"
        except Exception as e:
            reply = f"⚠️ Unexpected error: {str(e)}"

    await cl.Message(content=f"💬 {reply}").send()