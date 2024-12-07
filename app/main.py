from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    "Root endpoint of the API"
    return {"message": "Welcome to URL Shortner Service"}