"""
Physical AI & Humanoid Robotics Textbook - Backend API
FastAPI server with RAG chat, auth, personalization, and translation.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

load_dotenv()

from auth import init_db, signup, signin, signout
from rag import chat, personalize_content, translate_content


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    history: list[dict] | None = None
    selected_text: str | None = None

class ChatResponse(BaseModel):
    response: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    background: dict | None = None

class SigninRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user: dict
    session_token: str

class PersonalizeRequest(BaseModel):
    content: str
    user_background: dict

class PersonalizeResponse(BaseModel):
    personalized_content: str

class TranslateRequest(BaseModel):
    content: str
    target_language: str = "urdu"

class TranslateResponse(BaseModel):
    translated_content: str


# ---------------------------------------------------------------------------
# App Lifecycle
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    init_db()
    yield


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Physical AI Textbook API",
    description="Backend API for Physical AI & Humanoid Robotics textbook with RAG chat, auth, personalization, and translation.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "*",  # Allow all for development - restrict in production
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# API Key Validation
# ---------------------------------------------------------------------------

API_KEY = os.getenv("API_KEY", "password123")


def validate_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    """Validate API key from request header."""
    if x_api_key and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Physical AI Textbook API",
        "version": "1.0.0",
    }


# ---------------------------------------------------------------------------
# Chat Endpoint (RAG)
# ---------------------------------------------------------------------------

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    """RAG-based chat endpoint. Searches textbook content and generates answers."""
    validate_api_key(x_api_key)

    try:
        response = chat(
            message=request.message,
            history=request.history,
            selected_text=request.selected_text,
        )
        return ChatResponse(response=response)
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


# ---------------------------------------------------------------------------
# Auth Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/auth/signup", response_model=AuthResponse)
async def signup_endpoint(
    request: SignupRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    """Create a new user account with background profiling."""
    validate_api_key(x_api_key)

    try:
        result = signup(
            email=request.email,
            password=request.password,
            name=request.name,
            background=request.background or {},
        )
        return AuthResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


@app.post("/api/auth/signin", response_model=AuthResponse)
async def signin_endpoint(
    request: SigninRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    """Authenticate an existing user."""
    validate_api_key(x_api_key)

    try:
        result = signin(email=request.email, password=request.password)
        return AuthResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print(f"Signin error: {e}")
        raise HTTPException(status_code=500, detail=f"Signin failed: {str(e)}")


@app.post("/api/auth/signout")
async def signout_endpoint(
    session_token: str = Query(...),
):
    """Invalidate user session."""
    try:
        signout(session_token)
        return {"message": "Signed out successfully"}
    except Exception as e:
        print(f"Signout error: {e}")
        raise HTTPException(status_code=500, detail=f"Signout failed: {str(e)}")


# ---------------------------------------------------------------------------
# Personalization Endpoint
# ---------------------------------------------------------------------------

@app.post("/api/personalize", response_model=PersonalizeResponse)
async def personalize_endpoint(
    request: PersonalizeRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    """Personalize chapter content based on user background."""
    validate_api_key(x_api_key)

    try:
        result = personalize_content(
            content=request.content,
            user_background=request.user_background,
        )
        return PersonalizeResponse(personalized_content=result)
    except Exception as e:
        print(f"Personalize error: {e}")
        raise HTTPException(status_code=500, detail=f"Personalization failed: {str(e)}")


# ---------------------------------------------------------------------------
# Translation Endpoint
# ---------------------------------------------------------------------------

@app.post("/api/translate", response_model=TranslateResponse)
async def translate_endpoint(
    request: TranslateRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    """Translate chapter content to target language (default: Urdu)."""
    validate_api_key(x_api_key)

    try:
        result = translate_content(
            content=request.content,
            target_language=request.target_language,
        )
        return TranslateResponse(translated_content=result)
    except Exception as e:
        print(f"Translate error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


# ---------------------------------------------------------------------------
# Run Server
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
