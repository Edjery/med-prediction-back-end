from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
)

@app.get("/")
async def read_root():
    return {
        "Hello There!": "Welcome to the Server!", 
        "For more info": "Please add '/docs' after the url", 
        "example": "http://127.0.0.1:8000/docs"
    }

@app.post("/predict/")
async def predict(text: str):
    return {"text": text}