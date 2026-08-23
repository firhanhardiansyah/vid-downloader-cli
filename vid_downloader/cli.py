import argparse
import json
import sys
from pathlib import Path

from vid_downloader import __version__
from vid_downloader.config_paths import (
    find_default_config_path,
    get_default_download_dir,
    get_global_config_path,
)
from vid_downloader.config_setup import configure_download_directory
from vid_downloader.download_config import load_download_config
from vid_downloader.interactive import collect_interactive_download
from vid_downloader.time_utils import parse_time_to_seconds


def main() -> None:
    parser = build_parser()
    args = parser.parse_args(normalize_command_alias(sys.argv[1:]))

    if args.version:
        print("Video Downloader Version:", __version__)
        raise SystemExit(0)

    if args.input == "config-path" and not args.download:
        print(find_default_config_path())
        raise SystemExit(0)

    if args.input == "init" and not args.download:
        config_path = args.config or get_global_config_path()
        try:
            created_path = configure_download_directory(config_path)
        except (EOFError, KeyboardInterrupt):
            print("\nConfiguration cancelled.")
            raise SystemExit(0)
        except ValueError as exc:
            print(exc)
            raise SystemExit(1)

        if created_path:
            print(f"Saved config: {created_path}")
        raise SystemExit(0)

    default_config_path = (
        Path(args.config or find_default_config_path()).expanduser().resolve()
    )

    if not args.download:
        if _needs_first_run_setup(args.config, default_config_path):
            try:
                print("No global configuration found. Let's create one.")
                created_path = configure_download_directory(default_config_path)
            except (EOFError, KeyboardInterrupt):
                print("\nConfiguration cancelled.")
                raise SystemExit(0)
            except ValueError as exc:
                print(exc)
                raise SystemExit(1)

            if created_path:
                print(f"Saved config: {created_path}")
                print("")

        try:
            interactive = collect_interactive_download(
                parse_download_input,
                default_config_path=str(default_config_path),
            )
        except (EOFError, KeyboardInterrupt):
            print("\nDownload cancelled.")
            raise SystemExit(0)

        if interactive is None:
            raise SystemExit(0)

        execute_download(
            urls=interactive.urls,
            folder=interactive.folder,
            quality=interactive.quality,
            audio_only=interactive.audio_only,
            start_time=interactive.start_time,
            end_time=interactive.end_time,
        )
        return

    try:
        input_value = args.input or str(default_config_path)
        urls, config_download_dir, config_quality = parse_download_input(input_value)

        if args.input and not config_download_dir:
            try:
                _, default_dir, default_quality = parse_download_input(
                    str(default_config_path)
                )
                config_download_dir = default_dir
                config_quality = default_quality
            except ValueError:
                pass
        extra_headers = parse_extra_headers(args.headers)
        cookies_from_browser = parse_cookies_from_browser(args.cookies_browser)

        start_time = parse_time_to_seconds(args.start_time)
        end_time = parse_time_to_seconds(args.end_time)
        validate_time_range(start_time, end_time)

    except ValueError as exc:
        print(exc)
        raise SystemExit(1)

    execute_download(
        urls=urls,
        folder=(
            args.folder
            or config_download_dir
            or str(get_default_download_dir())
        ),
        quality=args.quality or config_quality or "best",
        audio_only=args.audio,
        simple=args.simple,
        referer=args.referer,
        cookies_from_browser=cookies_from_browser,
        extra_headers=extra_headers,
        filename_mode=args.filename_mode,
        start_time=start_time,
        end_time=end_time,
    )


def _needs_first_run_setup(
    explicit_config: str | None,
    selected_config: Path,
) -> bool:
    if explicit_config or selected_config.exists():
        return False

    return selected_config == get_global_config_path().resolve()


def execute_download(
    urls: list[str],
    folder: str,
    quality: str,
    audio_only: bool = False,
    simple: bool = False,
    referer: str | None = None,
    cookies_from_browser: tuple[str] | None = None,
    extra_headers: dict | None = None,
    filename_mode: str = "title",
    start_time: int | float | None = None,
    end_time: int | float | None = None,
) -> None:
    from vid_downloader.download_lock import DownloadDirectoryBusyError
    from vid_downloader.downloader import download_videos

    try:
        download_videos(
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
    except DownloadDirectoryBusyError as exc:
        print(exc)
        raise SystemExit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Video Downloader CLI")

    parser.add_argument(
        "--download",
        action="store_true",
        help="Start downloading using download.conf or the provided input",
    )
    parser.add_argument(
        "--config",
        help="Use a specific download config file",
    )
    parser.add_argument(
        "input",
        nargs="?",
        help=(
            "Video URL, config file, or command: download/init/config-path"
        ),
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=["144", "240", "360", "480", "720", "1080", "best"],
        help="Override QUALITY: 144, 240, 360, 480, 720, 1080, or best",
    )
    parser.add_argument(
        "-a",
        "--audio",
        action="store_true",
        help="Download audio only as MP3 (192 kbps)",
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
        help="Override DOWNLOAD_DIR from the config file",
    )
    parser.add_argument(
        "--filename-mode",
        default="title",
        choices=["title_id", "title", "id"],
        help="Filename format: title (default), title_id, or id",
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


def normalize_command_alias(arguments: list[str]) -> list[str]:
    if arguments and arguments[0] == "download":
        return ["--download", *arguments[1:]]

    return arguments


def parse_download_input(
    input_value: str,
) -> tuple[list[str], str | None, str | None]:
    if input_value.endswith((".conf", ".config")):
        config = load_download_config(input_value)
        return config.urls, config.download_dir, config.quality

    if input_value.endswith(".txt"):
        with open(input_value, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        if not input_value.startswith(("http://", "https://")):
            raise ValueError("Input must be an http:// or https:// URL.")
        urls = [input_value]

    if not urls:
        raise ValueError("No valid URLs found.")

    return urls, None, None


def parse_input_urls(input_value: str) -> list[str]:
    """Backward-compatible helper for callers that only need URLs."""
    urls, _, _ = parse_download_input(input_value)
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
