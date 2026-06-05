"""
FastAPI application entry point.
Initializes the app, middleware, routes, and exception handlers.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.routes import router
from src.config.settings import ensure_data_dirs
from src.ingestion.embedder import get_vectorstore
from src.ingestion.scheduler import init_scheduler, shutdown_scheduler

# Configure standard library logging for the app
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events for the FastAPI application.
    """
    logger.info("Starting up Mutual Fund FAQ Assistant API...")
    
    # Ensure necessary directories exist
    ensure_data_dirs()
    
    # Pre-load the vector store and embedding model on startup
    # This prevents the first request from suffering initialization latency
    try:
        logger.info("Initializing vector store and embedding model...")
        _ = get_vectorstore()
        logger.info("Vector store initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize vector store on startup: {e}")
        # We don't raise here; if it fails, it will retry on the first query
        
    # Start the background scheduler
    init_scheduler()

    yield
    
    logger.info("Shutting down API...")
    shutdown_scheduler()


app = FastAPI(
    title="Mutual Fund FAQ Assistant",
    description="RAG-powered API for answering factual questions about HDFC mutual funds.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ───────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# ── Exception Handlers ───────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return a graceful JSON response."""
    logger.error(f"Unhandled exception during {request.method} {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal server error occurred.",
            "detail": str(exc)
        }
    )


# ── Routes ───────────────────────────────────────────────────────────────────

# Mount API routes
app.include_router(router, prefix="/api", tags=["API"])

# Mount static files for the frontend UI
# Ensure the `frontend` directory exists or this will raise a RuntimeError at startup
import os
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    logger.warning(f"Frontend directory not found at {frontend_dir}. Static files will not be served.")
