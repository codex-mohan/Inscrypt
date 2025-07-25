"""
Inscrypt API - FastAPI backend for steganography system
Provides encryption, hashing, and steganography services
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import InscryptException

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Inscrypt API...")

    # Create necessary directories
    Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
    Path(settings.TEMP_DIR).mkdir(exist_ok=True)
    Path(settings.OUTPUT_DIR).mkdir(exist_ok=True)

    logger.info("Inscrypt API started successfully")
    yield

    logger.info("Shutting down Inscrypt API...")
    # Cleanup temporary files
    import shutil

    if Path(settings.TEMP_DIR).exists():
        shutil.rmtree(settings.TEMP_DIR)
    logger.info("Inscrypt API shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Inscrypt API",
    description="Advanced steganography system with encryption and hashing services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(InscryptException)
async def inscrypt_exception_handler(request, exc: InscryptException):
    """Handle custom Inscrypt exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.error_code},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500, content={"detail": "An unexpected error occurred"}
    )


# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Mount static files for downloads
app.mount("/downloads", StaticFiles(directory=settings.OUTPUT_DIR), name="downloads")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Inscrypt API",
        "version": "1.0.0",
        "description": "Advanced steganography system with encryption and hashing services",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "inscrypt-api", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
