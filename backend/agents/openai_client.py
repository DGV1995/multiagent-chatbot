from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI

from backend.__init__ import (
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    OPENAI_API_VERSION,
)

# from openai import AzureOpenAI


_openai_client = None


def get_openai_client():
    """
    Lazily initializes and returns a singleton AzureOpenAI client instance.
    Raises ValueError if required environment variables are missing.
    """
    global _openai_client
    if not _openai_client:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )

        _openai_client = AzureChatOpenAI(
            azure_deployment=AZURE_OPENAI_DEPLOYMENT,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider=token_provider,
            api_version=OPENAI_API_VERSION,
        )
    return _openai_client
