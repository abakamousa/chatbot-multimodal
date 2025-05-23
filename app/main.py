import chainlit as cl
import httpx
import os

AZURE_FUNCTION_URL = "http://localhost:7071/api/chatbot" #os.getenv("AZURE_FUNCTION_URL")  # e.g., "https://your-func-name.azurewebsites.net/api/chatbot"

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hello! I'm your assistant. How can I help you today?").send()

@cl.on_message
async def on_message(message: cl.Message):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                AZURE_FUNCTION_URL,
                json={"message": message.content},
                timeout=30
            )
            res.raise_for_status()
            data = res.json()
            reply = data.get("response", "No response.")
        except httpx.HTTPStatusError as e:
            reply = f"❌ Error: {e.response.json().get('error', str(e))}"
        except Exception as e:
            reply = f"⚠️ Unexpected error: {str(e)}"

    await cl.Message(content=f"💬 {reply}").send()
