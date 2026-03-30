import argparse
import json

from core import __version__
from core.downloader import download_videos

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
    help="Video quality: 360, 480, 720, 1080, or best",
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

args = parser.parse_args()

# Show version
if args.version:
    print("Video Downloader Version:", __version__)
    raise SystemExit(0)

# Validate input
if not args.input:
    print("Please provide a video URL or a .txt file containing URLs.")
    raise SystemExit(1)

# Read URLs from input
if args.input.endswith(".txt"):
    with open(args.input, "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]
else:
    urls = [args.input]

# Parse extra headers
extra_headers = None
if args.headers:
    try:
        extra_headers = json.loads(args.headers)
        if not isinstance(extra_headers, dict):
            raise ValueError("Headers must be a JSON object.")
    except Exception as exc:
        print(f"Invalid --headers value: {exc}")
        raise SystemExit(1)

# Parse browser cookies
cookies_from_browser = None
if args.cookies_browser:
    cookies_from_browser = (args.cookies_browser,)

# Start download
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
)