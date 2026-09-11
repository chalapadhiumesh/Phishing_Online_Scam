from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine
from .models import Base
from .core.config import settings
from .services.ml_service import ml_service

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML models
    ml_service.load_models()
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

from .routers import auth, dashboard, scanner, history

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        settings.FRONTEND_URL
    ] if settings.FRONTEND_URL else [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(scanner.router)
app.include_router(history.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phishing & Scam Intelligence Platform API"}
