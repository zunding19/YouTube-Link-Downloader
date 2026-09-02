from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import yt_dlp
import os
import uuid
import glob


os.makedirs("downloads", exist_ok=True)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


class VideoRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return FileResponse("static/index.html")


def remove_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


@app.post("/download")
def download_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks
):

    url = request.url.strip()

    if not url:
        raise HTTPException(
            status_code=400,
            detail="Please enter a YouTube URL."
        )

    if "youtube.com" not in url and "youtu.be" not in url:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid YouTube URL."
        )

    unique_id = str(uuid.uuid4())

    output_template = f"downloads/{unique_id}.%(ext)s"

    options = {

        "outtmpl": output_template,

        "format": "bestvideo*+bestaudio/best",

        "merge_output_format": "mp4",

        "noplaylist": True,

        "js_runtimes": {
            "node": {
                "path": "/usr/local/bin/node"
            }
        },

        "extractor_args": {

            "youtube": {
                "player_client": ["mweb"]
            },

            "youtubepot-bgutilscript": {
                "server_home": [
                    "/opt/bgutil-ytdlp-pot-provider/server"
                ]
            }

        },

    }

    try:

        with yt_dlp.YoutubeDL(options) as ydl:

            ydl.extract_info(
                url,
                download=True
            )

        files = glob.glob(
            f"downloads/{unique_id}.*"
        )

        if not files:

            raise Exception(
                "The downloaded video file could not be found."
            )

        downloaded_file = files[0]

        background_tasks.add_task(
            remove_file,
            downloaded_file
        )

        return FileResponse(
            path=downloaded_file,
            filename="youtube-video.mp4",
            media_type="video/mp4",
            background=background_tasks
        )

    except Exception as error:

        print(
            "DOWNLOAD ERROR:",
            repr(error)
        )

        leftover_files = glob.glob(
            f"downloads/{unique_id}.*"
        )

        for file in leftover_files:
            remove_file(file)

        error_text = str(error).lower()

        if (
            "sign in to confirm" in error_text
            or
            "not a bot" in error_text
        ):

            message = (
                "YouTube temporarily blocked this server request. "
                "Please try again later."
            )

        elif "private video" in error_text:

            message = (
                "This video is private and cannot be downloaded."
            )

        elif "video unavailable" in error_text:

            message = (
                "This video is unavailable."
            )

        else:

            message = (
                "Unable to download this video. "
                "Please try another public YouTube video."
            )

        raise HTTPException(
            status_code=400,
            detail=message
        )