import os

import imageio_ffmpeg
import yt_dlp

from core.utils import ensure_folder

def download_videos(
    urls,
    folder="videos",
    quality="best",
    audio_only=False,
    simple=False,
    referer=None,
    cookies_from_browser=None,  # example: ('chrome',) or ('firefox',)
    extra_headers=None,
    filename_mode="title_id",  # "title_id" | "title" | "id"
):
    ensure_folder(folder)

    if audio_only:
        format_option = "bestaudio/best"
    else:
        if simple:
            format_option = "best"
        else:
            if quality == "best":
                format_option = "bestvideo+bestaudio/best"
            else:
                format_option = f"bestvideo[height<={quality}]+bestaudio/best"

    http_headers = extra_headers.copy() if extra_headers else {}
    if referer:
        http_headers["Referer"] = referer

    output_template = build_output_template(folder, filename_mode)

    ydl_opts = {
        "format": format_option,
        "merge_output_format": "mp4",
        "outtmpl": output_template,
        "noplaylist": True,
        "ignoreerrors": True,
        "retries": 10,
        "continuedl": True,
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "http_headers": http_headers,
        "overwrites": False,
    }

    if cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = cookies_from_browser

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def build_output_template(folder: str, filename_mode: str) -> str:
    templates = {
        "title_id": "%(title).200s [%(id)s].%(ext)s",
        "title": "%(title).200s.%(ext)s",
        "id": "%(id)s.%(ext)s",
    }

    if filename_mode not in templates:
        raise ValueError(
            "Invalid filename_mode. Use one of: 'title_id', 'title', or 'id'."
        )

    return os.path.join(folder, templates[filename_mode])