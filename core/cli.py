import argparse
import json

from core import __version__
from core.downloader import download_videos
from core.time_utils import parse_time_to_seconds


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print("Video Downloader Version:", __version__)
        raise SystemExit(0)

    if not args.input:
        print("Please provide a video URL or a .txt file containing URLs.")
        raise SystemExit(1)

    try:
        urls = parse_input_urls(args.input)
        extra_headers = parse_extra_headers(args.headers)
        cookies_from_browser = parse_cookies_from_browser(args.cookies_browser)

        start_time = parse_time_to_seconds(args.start_time)
        end_time = parse_time_to_seconds(args.end_time)
        validate_time_range(start_time, end_time)

    except ValueError as exc:
        print(exc)
        raise SystemExit(1)

    download_videos(
        urls=urls,
        folder=args.folder,
        quality=args.quality,
        audio_only=args.audio,
        simple=args.simple,
        referer=args.referer,
        cookies_from_browser=cookies_from_browser,
        extra_headers=extra_headers,
        filename_mode=args.filename_mode,
        start_time=start_time,
        end_time=end_time,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Video Downloader CLI")

    parser.add_argument(
        "input",
        nargs="?",
        help="Video URL or a .txt file containing URLs",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default="best",
        help="Video quality: 144, 240, 360, 480, 720, 1080, or best",
    )
    parser.add_argument(
        "-a",
        "--audio",
        action="store_true",
        help="Download audio only",
    )
    parser.add_argument(
        "-s",
        "--simple",
        action="store_true",
        help="Enable simple mode for faster download",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show application version",
    )

    # Output settings
    parser.add_argument(
        "-f",
        "--folder",
        default="videos",
        help="Output folder for downloaded files",
    )
    parser.add_argument(
        "--filename-mode",
        default="title_id",
        choices=["title_id", "title", "id"],
        help="Filename format: title_id, title, or id",
    )

    # Additional options for embedded/modal/protected sources
    parser.add_argument(
        "-r",
        "--referer",
        help="Referer URL, useful for embedded or modal videos",
    )
    parser.add_argument(
        "-c",
        "--cookies-browser",
        choices=["chrome", "firefox", "edge", "brave", "opera", "chromium", "safari"],
        help="Load cookies from a browser session",
    )
    parser.add_argument(
        "--headers",
        help='Extra HTTP headers in JSON format, for example: \'{"User-Agent":"Mozilla/5.0"}\'',
    )

    # Partial download options
    parser.add_argument(
        "--start",
        "--start-time",
        dest="start_time",
        help=(
            "Start time for partial download. "
            "Supported formats: seconds, MM:SS, or HH:MM:SS. "
            'Examples: "90", "01:30", "00:01:30".'
        ),
    )

    parser.add_argument(
        "--end",
        "--end-time",
        dest="end_time",
        help=(
            "End time for partial download. "
            "Supported formats: seconds, MM:SS, or HH:MM:SS. "
            'Examples: "180", "03:00", "00:03:00".'
        ),
    )

    return parser


def parse_input_urls(input_value: str) -> list[str]:
    if input_value.endswith(".txt"):
        with open(input_value, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        urls = [input_value]

    if not urls:
        raise ValueError("No valid URLs found.")

    return urls


def parse_extra_headers(headers: str | None) -> dict | None:
    if not headers:
        return None

    try:
        extra_headers = json.loads(headers)

        if not isinstance(extra_headers, dict):
            raise ValueError("Headers must be a JSON object.")

        return extra_headers

    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid --headers value: {exc}") from exc


def parse_cookies_from_browser(browser: str | None) -> tuple[str] | None:
    if not browser:
        return None

    return (browser,)


def validate_time_range(
    start_time: int | float | None,
    end_time: int | float | None,
) -> None:
    if start_time is not None and start_time < 0:
        raise ValueError("Invalid --start value: must be 0 or greater.")

    if end_time is not None and end_time < 0:
        raise ValueError("Invalid --end value: must be 0 or greater.")

    if start_time is not None and end_time is not None and start_time >= end_time:
        raise ValueError("Invalid range: --start must be less than --end.")