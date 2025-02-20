import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import Config
from routes.house_router import router as house_router

def create_app () -> FastAPI:
    
    """
    Factory function to create and configure the FastAPI application.

    This function initializes the FastAPI app with settings from the `Config` class, configures 
    CORS middleware with environment variable settings, and includes the house router for the API.

    The function returns the configured FastAPI application instance.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    
    app = FastAPI (
        title=Config.TITLE,
        description=Config.DESCRIPTION,
        version=Config.VERSION,
    )

    app.add_middleware (
        CORSMiddleware,
        allow_origins=os.getenv('FASTAPI_ALLOW_ORIGINS'), 
        allow_credentials=os.getenv('FASTAPI_ALLOW_CREDENTIALS'),
        allow_methods=os.getenv('FASTAPI_ALLOW_METHODS'),
        allow_headers=os.getenv('FASTAPI_ALLOW_HEADERS'),
    )

    app.include_router(house_router)

    return app
