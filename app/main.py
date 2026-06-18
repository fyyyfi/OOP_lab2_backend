"""Application factory and front controller.

FastAPI itself acts as the front controller: every HTTP request enters here
and is dispatched to the matching controller via the registered routers
(route patterns such as ``/api/requests/{request_id}``).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    auth_controller,
    brigade_controller,
    request_controller,
    specialist_controller,
)
from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register controllers (routing / dispatch table).
    app.include_router(auth_controller.router)
    app.include_router(request_controller.router)
    app.include_router(specialist_controller.router)
    app.include_router(brigade_controller.router)

    @app.get("/api/health", tags=["health"])
    def health() -> dict:
        return {"status": "ok"}

    logger.info("Application '%s' initialised", settings.app_name)
    return app


app = create_app()
