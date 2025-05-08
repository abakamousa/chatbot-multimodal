from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from app.config.settings import get_settings

settings = get_settings()

llm = AzureChatOpenAI(
    deployment_name=settings.azure_openai_deployment_name,
    openai_api_key=settings.azure_openai_api_key,
    openai_api_base=settings.azure_openai_endpoint,
    openai_api_version="2023-07-01-preview",  # match your Azure config
    openai_api_type="azure",
    temperature=0.7
)

def chat_with_agent(user_input: str) -> str:
    messages = [
        HumanMessage(content=user_input)
    ]
    response = llm(messages)
    return response.content
