from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Init
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Validation
class PredictionRequest(BaseModel):
    inputText: str

# API methods
@app.get("/")
async def read_root():
    return {
        "Hello There!": "Welcome to the Server!", 
        "For more info": "Please add '/docs' after the url", 
        "example": "http://127.0.0.1:8000/docs"
    }

@app.post("/predict/")
async def predict(request: PredictionRequest):
    return request