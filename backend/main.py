import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Adjust these imports based on the folder structure I gave you
from app import models
from app.db.session import engine, SessionLocal

from app.db.seed_components import seed_components
# Assuming you put your router in app/api/v1/router.py
from app.api.v1.router import api_router 
from config import settings

# ✅ LIFESPAN: The correct way to handle async startup tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up Workflow Builder...")
    
    # Create DB tables (Async compatible)
    async with engine.begin() as conn:
        # run_sync allows us to use the synchronous create_all method 
        # inside the async context
        await conn.run_sync(models.Base.metadata.create_all)

    async with SessionLocal() as session:
        await seed_components(session)
    
    yield
    
    print("🛑 Shutting down...")
    # Add cleanup logic here if needed (e.g., closing connections)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Low-Code/No-Code Workflow Engine with RAG & LLM integration",
    version="1.0.0",
    lifespan=lifespan, # Register the lifespan handler
    # debug=settings.debug # Note: 'debug' param is deprecated in newer FastAPI versions
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Update this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Ensure settings.API_PORT / API_HOST exist in your config.py
    # or default to standard values
    uvicorn.run(
        "main:app", # Note: 'app.main:app' assumes running from root
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )