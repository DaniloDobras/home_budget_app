from fastapi import FastAPI

from app.api import auth, categories, bills, statistics
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Home Budget",
    openapi_version="3.0.3",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(bills.router)
app.include_router(statistics.router)
