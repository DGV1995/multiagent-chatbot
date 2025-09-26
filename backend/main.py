import os
from typing import List

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Chatbot API", version="1.0.0")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Azure OpenAI client
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_ad_token_provider=token_provider,
    api_version=os.getenv("OPENAI_API_VERSION", "2024-10-21"),
)


class ChatMessage(BaseModel):
    message: str
    history: List[dict] = []


class ChatResponse(BaseModel):
    response: str
    success: bool


@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}


@app.get("/health/azure")
async def azure_health():
    """Check Azure OpenAI connectivity and configuration"""
    try:
        # Check if all required environment variables are set
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        missing_vars = []
        if not api_key:
            missing_vars.append("AZURE_OPENAI_API_KEY")
        if not endpoint:
            missing_vars.append("AZURE_OPENAI_ENDPOINT")
        if not api_version:
            missing_vars.append("AZURE_OPENAI_API_VERSION")
        if not deployment:
            missing_vars.append("AZURE_OPENAI_DEPLOYMENT_NAME")

        if missing_vars:
            return {
                "status": "error",
                "message": f"Missing environment variables: {', '.join(missing_vars)}",
            }

        # Test a simple completion
        _ = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10,
        )

        return {
            "status": "healthy",
            "message": "Azure OpenAI connection successful",
            "endpoint": endpoint,
            "deployment": deployment,
            "api_version": api_version,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Azure OpenAI connection failed: {str(e)}",
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_data: ChatMessage):
    try:
        # Build conversation history for OpenAI
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        # Add previous messages from history
        for msg in chat_data.history:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})

        # Add current message
        messages.append({"role": "user", "content": chat_data.message})

        # Call Azure OpenAI API
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-20240806"),
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        ai_response = response.choices[0].message.content

        return ChatResponse(response=ai_response, success=True)

    except Exception as e:
        # Log the specific error for debugging
        error_message = f"Error processing request: {str(e)}"
        print(f"DEBUG - Azure OpenAI Error: {error_message}")
        print(
            f"DEBUG - API Key exists: {'Yes' if os.getenv('AZURE_OPENAI_API_KEY') else 'No'}"
        )
        print(f"DEBUG - Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
        print(f"DEBUG - Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
        print(f"DEBUG - API Version: {os.getenv('AZURE_OPENAI_API_VERSION')}")

        raise HTTPException(status_code=500, detail=error_message)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
