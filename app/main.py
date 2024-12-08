from fastapi import FastAPI
from .routers.urls_router import router as urls_router
from .routers.urls_router import redirect_router as redirect_router
from .routers.analytics_router import router as analytics_router

app = FastAPI()

app.include_router(urls_router, prefix="/api/urls", tags=["URL Operations"])
app.include_router(redirect_router, prefix="", tags=["URL Redirect"])
app.include_router(analytics_router, prefix="/api/urls", tags=["Analytics Operations"])

@app.get("/")
async def root():
    "Root endpoint of the API"
    return {"message": "Welcome to URL Shortner Service"}