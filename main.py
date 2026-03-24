import argparse
from core import __version__
from core.downloader import download_videos

parser = argparse.ArgumentParser(description="Video Downloader CLI")

parser.add_argument("input", nargs="?", help="Video URL or .txt file containing URLs")
parser.add_argument("-q", "--quality", default="best", help="Video quality: 360, 480, 720, 1080, best")
parser.add_argument("-a", "--audio", action="store_true", help="Download audio only")
parser.add_argument("-s", "--simple", action="store_true", help="Simple mode (fast download)")
parser.add_argument("-v", "--version", action="store_true", help="Show application version")

args = parser.parse_args()

# Show version
if args.version:
    print("Video Downloader Version:", __version__)
    exit()

# Check input
if not args.input:
    print("Please provide a video URL or a .txt file containing URLs.")
    exit()

# Read URLs
if args.input.endswith(".txt"):
    with open(args.input, "r") as file:
        urls = [line.strip() for line in file if line.strip()]
else:
    urls = [args.input]

# Start download
download_videos(
    urls,
    quality=args.quality,
    audio_only=args.audio,
    simple=args.simple
)