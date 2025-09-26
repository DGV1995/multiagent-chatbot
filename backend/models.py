from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str
    history: list[dict] = []


class ChatResponse(BaseModel):
    response: str
    success: bool
