import os
import json
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
ROUTER_API_KEY = os.getenv("ROUTER_API_KEY")

if ROUTER_API_KEY is None:
    raise ValueError("ROUTER_API_KEY not found. Please check your .env file.")

# Load context.json for bot knowledge base
with open("context.json", "r") as file:
    context = json.load(file)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware with logging and broader configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://100rabhsah-ai-assistant.vercel.app", "http://localhost:3000"],  # Trusted origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods like POST, GET, OPTIONS
    allow_headers=["*"],  # Allow all headers
)

class ChatRequest(BaseModel):
    query: str

# Define strict system prompt
SYSTEM_PROMPT = (
    "You are Sourabh Sah’s personal AI assistant. You can ONLY answer questions about Sourabh Sah — his background, skills, projects, philosophy, achievements, and values. "
    "All of this information is loaded from the provided context. "
    "You MUST NOT answer anything about other people, celebrities, or give opinions not grounded in this context. "
    "If a question is outside your knowledge, respond with: "
    "\"Sorry, I can only talk about Sourabh Sah based on provided context.\""
)

BASE_URL = "https://router.requesty.ai/v1"

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    user_query = payload.query.strip()

    # Build messages for context injection
    context_messages = [{"role": "assistant", "content": entry} for entry in context]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + context_messages + [
        {"role": "user", "content": user_query}
    ]

    headers = {
        "Authorization": f"Bearer {ROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemini-2.0-flash-exp",
        "messages": messages
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)

        if response.status_code != 200:
            print(f"Error response from API: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Requestly API error: {response.text}")

        assistant_response = response.json()["choices"][0]["message"]["content"]

        return {"response": assistant_response}

    except requests.RequestException as e:
        print(f"RequestException: {e}")
        raise HTTPException(status_code=500, detail=f"Requestly API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# Handle OPTIONS (preflight) requests
@app.options("/chat")
async def options_request():
    return {
        "access-control-allow-origin": "https://100rabhsah-ai-assistant.vercel.app",
        "access-control-allow-methods": "POST, OPTIONS",
        "access-control-allow-headers": "Content-Type",
        "access-control-allow-credentials": "true"
    }

# Logging Origin Header for Debugging
@app.middleware("http")
async def log_origin(request, call_next):
    origin = request.headers.get("origin")
    print(f"Received request with Origin: {origin}")  # Log incoming request's Origin header
    response = await call_next(request)
    return response
