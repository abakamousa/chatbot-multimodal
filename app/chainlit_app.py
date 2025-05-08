import chainlit as cl
from app.services.azure_openai import AzureOpenAIWrapper
from app.llm_validators.prompt_injection import PromptInjectionValidator
from app.llm_validators.answer_relevance import AnswerRelevanceValidator

# Initialize services and validators
ai = AzureOpenAIWrapper()
input_validators = [PromptInjectionValidator()]
output_validators = [AnswerRelevanceValidator()]

def run_validators(text: str, validators):
    for validator in validators:
        result = validator.validate(text)
        if not result.get("valid", True):
            return result  # Return first failure
    return {"valid": True}

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Hello! I'm your AI assistant. Ask me anything.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    # Validate the user input before sending to model
    input_check = run_validators(message.content, input_validators)
    if not input_check["valid"]:
        await cl.Message(content=f"⚠️ Input blocked: {input_check['reason']}").send()
        return

    try:
        messages = [{"role": "user", "content": message.content}]
        response = ai.chat_completion(messages)

        # Validate model response
        output_check = run_validators(response, output_validators)
        if not output_check["valid"]:
            await cl.Message(content=f"⚠️ Response flagged: {output_check['reason']}").send()
            return

        await cl.Message(content=response).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
