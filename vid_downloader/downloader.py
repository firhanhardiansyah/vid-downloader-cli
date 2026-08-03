import os

import imageio_ffmpeg
import yt_dlp
from yt_dlp.utils import download_range_func

from vid_downloader.config_paths import get_default_download_dir
from vid_downloader.download_lock import DownloadDirectoryLock
from vid_downloader.formats import build_format_option
from vid_downloader.metadata import print_video_info
from vid_downloader.time_utils import resolve_download_range
from vid_downloader.utils import ensure_folder


def download_videos(
    urls,
    folder=None,
    quality="best",
    audio_only=False,
    simple=False,
    referer=None,
    cookies_from_browser=None,
    extra_headers=None,
    filename_mode="title",
    start_time=None,
    end_time=None,
):
    folder = folder or str(get_default_download_dir())
    ensure_folder(folder)

    with DownloadDirectoryLock(folder):
        _download_videos_unlocked(
            urls=urls,
            folder=folder,
            quality=quality,
            audio_only=audio_only,
            simple=simple,
            referer=referer,
            cookies_from_browser=cookies_from_browser,
            extra_headers=extra_headers,
            filename_mode=filename_mode,
            start_time=start_time,
            end_time=end_time,
        )


def _download_videos_unlocked(
    urls,
    folder,
    quality,
    audio_only,
    simple,
    referer,
    cookies_from_browser,
    extra_headers,
    filename_mode,
    start_time,
    end_time,
):
    is_partial_requested = start_time is not None or end_time is not None

    format_option = build_format_option(
        quality=quality,
        audio_only=audio_only,
        simple=simple,
        is_partial_requested=is_partial_requested,
    )

    http_headers = extra_headers.copy() if extra_headers else {}
    if referer:
        http_headers["Referer"] = referer

    ydl_opts = {
        "format": format_option,
        "merge_output_format": "mp4",
        "outtmpl": build_output_template(folder, filename_mode),
        "noplaylist": True,
        "ignoreerrors": False,
        "retries": 10,
        "continuedl": True,
        "nopart": False,
        "keep_fragments": False,
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "http_headers": http_headers,
        "overwrites": False,
        "verbose": False,
        "extractor_args": {
            "generic": {"impersonate": ["chrome"]},
        },
    }

    if cookies_from_browser:
        ydl_opts["cookiesfrombrowser"] = cookies_from_browser

    total_urls = len(urls)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for index, url in enumerate(urls, start=1):
            info = ydl.extract_info(url, download=False)

            if is_partial_requested:
                duration = info.get("duration")
                resolved_start, resolved_end = resolve_download_range(
                    duration=duration,
                    start_time=start_time,
                    end_time=end_time,
                )

                ydl.params["download_ranges"] = download_range_func(
                    [],
                    [(resolved_start, resolved_end)],
                )

                print_video_info(
                    info,
                    index=index,
                    total=total_urls,
                    is_partial_requested=True,
                    start_time=resolved_start,
                    end_time=resolved_end,
                )
            else:
                print_video_info(
                    info,
                    index=index,
                    total=total_urls,
                )

            print("\nStarting download...")
            ydl.download([url])


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
