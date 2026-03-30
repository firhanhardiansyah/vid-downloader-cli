import argparse
import json
from core import __version__
from core.downloader import download_videos

parser = argparse.ArgumentParser(description="Video Downloader CLI")

parser.add_argument("input", nargs="?", help="Video URL or .txt file containing URLs")
parser.add_argument("-q", "--quality", default="best", help="Video quality: 360, 480, 720, 1080, best")
parser.add_argument("-a", "--audio", action="store_true", help="Download audio only")
parser.add_argument("-s", "--simple", action="store_true", help="Simple mode (fast download)")
parser.add_argument("-v", "--version", action="store_true", help="Show application version")

# tambahan untuk case popup/modal/protected source
parser.add_argument("-r", "--referer", help="Referer URL, useful for embedded/modal video")
parser.add_argument(
    "-c",
    "--cookies-browser",
    choices=["chrome", "firefox", "edge", "brave", "opera", "chromium", "safari"],
    help="Load cookies from browser session"
)
parser.add_argument(
    "--headers",
    help='Extra HTTP headers in JSON format, example: \'{"User-Agent":"Mozilla/5.0"}\''
)

args = parser.parse_args()

# Show version
if args.version:
    print("Video Downloader Version:", __version__)
    raise SystemExit(0)

# Check input
if not args.input:
    print("Please provide a video URL or a .txt file containing URLs.")
    raise SystemExit(1)

# Read URLs
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
            raise ValueError("Headers must be a JSON object")
    except Exception as e:
        print(f"Invalid --headers value: {e}")
        raise SystemExit(1)

# Parse cookies browser
cookies_from_browser = None
if args.cookies_browser:
    cookies_from_browser = (args.cookies_browser,)

# Start download
download_videos(
    urls=urls,
    folder="videos/movies",
    quality=args.quality,
    audio_only=args.audio,
    simple=args.simple,
    referer=args.referer,
    cookies_from_browser=cookies_from_browser,
    extra_headers=extra_headers,
)