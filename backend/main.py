import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.routers import api_router
from config import settings

import os

# Create DB tables at startup (safe to call multiple times)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Career Page Builder API",
    description="API for Career Page Builder application",
    version="1.0.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to Career Page Builder API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.api_port))
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
