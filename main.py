from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

class VideoRequest(BaseModel):
    url: str #expect some data containing url = string

@app.get("/") #when someone visits, run the function
def home():
    return {"message": "Backend is working"}

@app.post("/download")
def download_video(request: VideoRequest):

    url = request.url

    options = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s"
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        return {
            "message": "Download completed"
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

