"""
Main application module for FastAPI e-commerce REST API.

This module initializes the FastAPI application, registers all routers,
and configures global exception handlers.
"""
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from config.database import create_tables, engine
from config.logging_config import setup_logging
from config.redis_config import check_redis_connection, redis_config
from controllers.address_controller import AddressController
from controllers.auth_controller import auth_controller
from controllers.bill_controller import BillController
from controllers.category_controller import CategoryController
from controllers.client_controller import ClientController
from controllers.health_check import router as health_check_controller
from controllers.order_controller import OrderController
from controllers.order_detail_controller import OrderDetailController
from controllers.product_controller import ProductController
from controllers.review_controller import ReviewController
from middleware.rate_limiter import RateLimiterMiddleware
from middleware.request_id_middleware import RequestIDMiddleware
from repositories.base_repository_impl import InstanceNotFoundError

# Setup centralized logging FIRST
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    logger.info("🚀 Starting FastAPI E-commerce API...")
    if check_redis_connection():
        logger.info("✅ Redis cache is available")
    else:
        logger.warning("⚠️  Redis cache is NOT available - running without cache")
    yield
    logger.info("👋 Shutting down FastAPI E-commerce API...")
    try:
        redis_config.close()
        logger.info("✅ Redis connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing Redis: {e}")
    try:
        engine.dispose()
        logger.info("✅ Database engine disposed")
    except Exception as e:
        logger.error(f"❌ Error disposing database engine: {e}")
    logger.info("✅ Shutdown complete")

def create_fastapi_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    fastapi_app = FastAPI(
        title="E-commerce REST API",
        description="FastAPI REST API for e-commerce system with PostgreSQL",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Middleware (LIFO order)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Production: specify domains
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    fastapi_app.add_middleware(RateLimiterMiddleware, calls=100, period=60)
    fastapi_app.add_middleware(RequestIDMiddleware)

    # Global Exception Handlers
    @fastapi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors with a simplified 422 response."""
        try:
            first_error = exc.errors()[0]
            field = ".".join(map(str, first_error["loc"]))
            message = first_error["msg"]
            simplified_message = f"Error de validación: El campo '{field}' - {message}"
        except (IndexError, KeyError):
            simplified_message = "Error de validación en los datos de entrada."
        
        logger.error(f"Validation error for {request.method} {request.url}: {simplified_message}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": simplified_message},
        )

    @fastapi_app.exception_handler(InstanceNotFoundError)
    async def instance_not_found_handler(request: Request, exc: InstanceNotFoundError):
        """Handle InstanceNotFoundError with a 404 response."""
        logger.warning(f"Instance not found for {request.method} {request.url}: {exc}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )

    # Root endpoint
    @fastapi_app.get("/", tags=["Root"])
    def root():
        return {"status": "ok", "message": "API funcionando correctamente 🚀"}

    # Register all controllers
    fastapi_app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])
    client_controller = ClientController()
    fastapi_app.include_router(client_controller.router, prefix="/clients", tags=["Clients"])
    fastapi_app.include_router(OrderController().router, prefix="/orders", tags=["Orders"])
    fastapi_app.include_router(ProductController().router, prefix="/products", tags=["Products"])
    fastapi_app.include_router(AddressController().router, prefix="/addresses", tags=["Addresses"])
    fastapi_app.include_router(BillController().router, prefix="/bills", tags=["Bills"])
    fastapi_app.include_router(OrderDetailController().router, prefix="/order_details", tags=["Order Details"])
    fastapi_app.include_router(ReviewController().router, prefix="/reviews", tags=["Reviews"])
    fastapi_app.include_router(CategoryController().router, prefix="/categories", tags=["Categories"])
    fastapi_app.include_router(health_check_controller, prefix="/health_check", tags=["Health Check"])

    return fastapi_app

def run_app(fastapi_app: FastAPI):
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Create database tables on startup (for development)
    create_tables()
    app = create_fastapi_app()
    run_app(app)
