"""
NEX Brain API - FastAPI Application
Inteligentné rozhranie pre NEX ekosystém.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import chat

app = FastAPI(
    title="NEX Brain API",
    description="Inteligentné rozhranie pre NEX ekosystém",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    return {"service": "NEX Brain", "status": "running", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
