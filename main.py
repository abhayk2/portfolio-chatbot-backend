from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbotbackend import get_chat_response
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9002","https://abhay-spring.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# defines the structure of data we expect to receive from the frontend
class ChatRequest(BaseModel): #makes FastAPI automatically validate the incoming data
    messages:list #tells FastAPI to expect a messages field that is a list of chat messages


@app.post("/chat")
async def chat(request : ChatRequest):
    return StreamingResponse(
        get_chat_response(request.messages),
        media_type="text/event-stream",
        headers={
                    "X-Accel-Buffering": "no",
                    "Cache-Control": "no-cache",
                }
    )



