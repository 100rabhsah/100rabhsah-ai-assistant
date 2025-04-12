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

# ✅ Add CORS middleware immediately after app init
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (okay for dev, tighten for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

# Define system prompt
SYSTEM_PROMPT = (
    "You are Sourabh’s AI assistant. You can only answer questions about his professional path, "
    "projects, values, and personal growth based on documented context. "
    "You cannot share private info, speculate, or go beyond that scope."
)

BASE_URL = "https://router.requesty.ai/v1"  # Corrected base URL for Requestly

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    user_query = payload.query

    # Format the messages for the API request
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    headers = {
        "Authorization": f"Bearer {ROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Requestly (OpenRouter) API URL
    url = f"{BASE_URL}/chat/completions"
    
    data = {
        "model": "google/gemini-2.0-flash-exp",
        "messages": messages
    }

    try:
        # Make the API request to Requestly
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            # Log the full error response
            print(f"Error response from API: {response.text}")
            raise HTTPException(status_code=response.status_code, detail=f"Requestly API error: {response.text}")

        # Extract and return the response from the assistant
        assistant_response = response.json()["choices"][0]["message"]["content"]
        return {"response": assistant_response}

    except requests.RequestException as e:
        # Log the exception to help with debugging
        print(f"RequestException: {e}")
        raise HTTPException(status_code=500, detail=f"Requestly API error: {e}")
    except Exception as e:
        # Log any unexpected errors
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
