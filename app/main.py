from fastapi import FastAPI

from .configs.db_config import MongoDbDatabase
from .routers.urls_router import router as urls_router


app = FastAPI()

app.include_router(urls_router, prefix="/api/urls", tags=["URL Operations"])

@app.get("/")
async def root():
    "Root endpoint of the API"
    return {"message": "Welcome to URL Shortner Service"}