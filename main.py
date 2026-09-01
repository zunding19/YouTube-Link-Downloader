from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import yt_dlp
import os
import uuid

os.makedirs("downloads", exist_ok=True)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

class VideoRequest(BaseModel):
    url: str #expect some data containing url = string

@app.get("/") #when someone visits, run the function
def home():
    return FileResponse("static/index.html")

@app.post("/download")
def download_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks
):

    url = request.url

    unique_id = str(uuid.uuid4())

    output_template = f"downloads/{unique_id}.%(ext)s"

    options = {
        "outtmpl": output_template
    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            info = ydl.extract_info(url, download=True)

            downloaded_file = ydl.prepare_filename(info)


        background_tasks.add_task(
            os.remove,
            downloaded_file
        )


        return FileResponse(
            path=downloaded_file,
            filename=os.path.basename(downloaded_file),
            media_type="application/octet-stream"
        )


    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )