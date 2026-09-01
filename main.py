from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

class VideoRequest(BaseModel):
    url: str #expect some data containing url = string

@app.get("/") #when someone visits, run the function
def home():
    return {"message": "Backend is working"}
