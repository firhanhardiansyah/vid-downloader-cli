import os

import imageio_ffmpeg
import yt_dlp
from yt_dlp.utils import download_range_func

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
    filename_mode="title",  # "title_id" | "title" | "id"
    start_time=None,        # in seconds
    end_time=None,          # in seconds
):
    ensure_folder(folder)

    is_partial_requested = start_time is not None or end_time is not None

    if audio_only:
        format_option = "bestaudio/best"
    else:
        if is_partial_requested:
            # lebih aman untuk partial cut
            format_option = "best[ext=mp4]/best"
        elif simple:
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
        "ignoreerrors": False,
        "retries": 10,
        "continuedl": True,
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "http_headers": http_headers,
        "overwrites": False,
        "verbose": True,
        "extractor_args": {
            "generic": {"impersonate": ["chrome"]}
        },
    }

    if cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = cookies_from_browser

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if is_partial_requested:
            # ambil info dulu untuk dapat duration
            info = ydl.extract_info(urls[0], download=False)
            duration = info.get("duration")

            if duration is None:
                raise ValueError("Video duration is not available, so partial download cannot be resolved safely.")

            resolved_start = 0 if start_time is None else start_time
            resolved_end = duration if end_time is None else end_time

            if resolved_start < 0:
                raise ValueError("start_time must be 0 or greater.")
            if resolved_end < 0:
                raise ValueError("end_time must be 0 or greater.")
            if resolved_start >= resolved_end:
                raise ValueError("start_time must be less than end_time.")

            ydl.params["download_ranges"] = download_range_func(
                [],
                [(resolved_start, resolved_end)],
            )

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