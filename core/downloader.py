import yt_dlp
import os
import imageio_ffmpeg
from core.utils import ensure_folder

def download_videos(urls, folder="videos", quality="best", audio_only=False, simple=False):
    ensure_folder(folder)

    if audio_only:
        format_option = "bestaudio"
    else:
        if simple:
            format_option = "best"
        else:
            if quality == "best":
                format_option = "bestvideo+bestaudio/best"
            else:
                format_option = f"bestvideo[height<={quality}]+bestaudio/best"

    ydl_opts = {
        'format': format_option,
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ignoreerrors': True,
        'retries': 10,
        'continuedl': True,
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)