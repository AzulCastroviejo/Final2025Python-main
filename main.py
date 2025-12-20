# main.py - VERSIÓN CORREGIDA
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, base
from config.logging_config import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear tablas en la base de datos
base.metadata.create_all(bind=engine)

# Importar todos los controllers
from controllers.client_controller import ClientController
from controllers.product_controller import ProductController
from controllers.category_controller import CategoryController
from controllers.order_controller import OrderController
from controllers.order_detail_controller import OrderDetailController
from controllers.bill_controller import BillController
from controllers.address_controller import AddressController
from controllers.review_controller import ReviewController
from controllers.health_check import router as health_router

# Crear la aplicación FastAPI
app = FastAPI(
    title="E-commerce API",
    description="API REST para sistema de e-commerce",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers de los controllers
# IMPORTANTE: Asegúrate de que OrderController esté registrado
app.include_router(ClientController().router)
app.include_router(ProductController().router)
app.include_router(CategoryController().router)
app.include_router(OrderController().router)  # ✅ ESTA LÍNEA ES CRÍTICA
app.include_router(OrderDetailController().router)
app.include_router(BillController().router)
app.include_router(AddressController().router)
app.include_router(ReviewController().router)
app.include_router(health_router)

@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "message": "E-commerce API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health_check"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Solo para desarrollo
        log_level="info"
    )
