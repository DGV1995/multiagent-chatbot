import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends

from backend.agents.supervisor import get_supervisor
from backend.models import ChatMessage, ChatResponse

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


@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_data: ChatMessage, supervisor=Depends(get_supervisor)):
    try:
        # Build conversation history for OpenAI
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        # Add previous messages from history
        for msg in chat_data.history:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})

        # Add current message
        messages.append({"role": "user", "content": chat_data.message})

        # Call the supervisor agent
        result = supervisor.invoke({"messages": messages})

        # Clean backslashes
        ai_response = result["messages"][-1].content.replace("\\", "")

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
