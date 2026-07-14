"""
main.py

FastAPI entry point for the Drupal Enterprise AI Agent.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.search import router as search_router
from api.chat import router as chat_router

# ======================================================
# Create FastAPI Application
# ======================================================

app = FastAPI(
    title="Drupal Enterprise AI Agent",
    version="1.0.0",
    description="Enterprise AI Agent powered by Drupal CMS, Azure AI Search, Azure OpenAI GPT-5, and FastAPI.",
)

# ======================================================
# Enable CORS
# ======================================================
# NOTE:
# This allows your HTML UI (running on Live Server or another
# local server) to communicate with FastAPI.
#
# For production, replace "*" with your actual frontend URL.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Example: ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# Register API Routers
# ======================================================

app.include_router(search_router)
app.include_router(chat_router)

# ======================================================
# Root Endpoint
# ======================================================

@app.get("/", tags=["Home"])
def home():
    return {
        "application": "Drupal Enterprise AI Agent",
        "version": "1.0.0",
        "status": "Healthy",
        "message": "Drupal Enterprise AI Agent is running successfully.",
        "swagger_ui": "http://127.0.0.1:8000/docs",
    }

# ======================================================
# Health Check
# ======================================================

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "Healthy",
        "service": "FastAPI",
    }