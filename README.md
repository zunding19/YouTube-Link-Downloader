# YouTube Link Downloader

A simple web application that allows users to paste a YouTube URL and download the video directly through their browser.

## Live Demo

https://youtube-link-downloader.onrender.com

## Features

- Paste a YouTube video URL
- Download videos directly through the browser
- Simple and responsive user interface
- Backend video processing using yt-dlp
- FFmpeg integration for video and audio processing
- Temporary server-side file handling
- Dockerized for deployment
- Publicly deployed using Render

## Tech Stack

### Backend
- Python
- FastAPI
- yt-dlp
- FFmpeg

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Docker
- Render
- GitHub

## How It Works

1. The user enters a YouTube URL.
2. JavaScript sends the URL to the FastAPI backend.
3. The backend uses yt-dlp to retrieve and download the video.
4. FFmpeg handles video/audio processing when required.
5. FastAPI returns the completed file to the browser.
6. The temporary server-side file is removed after the download.

## Project Structure

```text
YouTube-Link-Downloader/
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/zunding19/YouTube-Link-Downloader.git
cd YouTube-Link-Downloader
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Make sure FFmpeg is installed.

On macOS:

```bash
brew install ffmpeg
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## What I Learned

Through this project, I gained practical experience with:

- Building REST API endpoints with FastAPI
- Connecting a JavaScript frontend to a Python backend
- Handling HTTP requests and file responses
- Working with yt-dlp and FFmpeg
- Managing temporary files on a server
- Using Python virtual environments and dependencies
- Containerizing an application with Docker
- Using Git and GitHub for version control
- Deploying a containerized web application to Render

## Author

Han Zun Ding