import yt_dlp

url = input("Youtube URL: ")

yt_dlp.YoutubeDL(
    {"format": "bestvideo+bestaudio/best"}
).download([url])