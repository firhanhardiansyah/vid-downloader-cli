import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from vid_downloader.config_paths import get_default_download_dir
from vid_downloader.time_utils import format_duration, parse_time_to_seconds


QUALITY_OPTIONS = {"144", "240", "360", "480", "720", "1080", "best"}


@dataclass(frozen=True)
class InteractiveDownload:
    urls: list[str]
    folder: str
    quality: str
    audio_only: bool
    start_time: int | float | None
    end_time: int | float | None


def collect_interactive_download(
    parse_input: Callable[[str], tuple[list[str], str | None, str | None]],
    default_config_path: str = "download.conf",
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> InteractiveDownload | None:
    output_func("Video Downloader")
    output_func("")

    default_folder, default_quality = _load_config_defaults(
        parse_input,
        default_config_path,
    )
    urls = _prompt_url(
        parse_input=parse_input,
        input_func=input_func,
        output_func=output_func,
    )
    use_advanced_options = _prompt_yes_no(
        "Advanced options? [y/N]: ",
        default=False,
        input_func=input_func,
        output_func=output_func,
    )

    folder = default_folder or str(get_default_download_dir())
    quality = default_quality or "best"
    audio_only = False
    start_time = None
    end_time = None

    if use_advanced_options:
        folder = _prompt_folder(default=folder, input_func=input_func)
        audio_only = _prompt_yes_no(
            "Audio only (MP3)? [y/N]: ",
            default=False,
            input_func=input_func,
            output_func=output_func,
        )
        if not audio_only:
            quality = _prompt_quality(
                default=quality,
                input_func=input_func,
                output_func=output_func,
            )
        start_time, end_time = _prompt_time_range(
            input_func=input_func,
            output_func=output_func,
        )

    output_func("")
    output_func("Download summary")
    output_func(f"URLs      : {len(urls)}")
    output_func(f"Directory : {folder}")
    output_func(f"Mode      : {'Audio' if audio_only else 'Video'}")
    if audio_only:
        output_func("Format    : MP3")
        output_func("Quality   : 192 kbps")
    else:
        output_func(f"Quality   : {quality}")
    output_func(
        f"Range     : {_format_range(start_time, end_time, audio_only)}"
    )
    output_func("")

    confirmed = _prompt_yes_no(
        "Start download? [Y/n]: ",
        default=True,
        input_func=input_func,
        output_func=output_func,
    )
    if not confirmed:
        output_func("Download cancelled.")
        return None

    return InteractiveDownload(
        urls=urls,
        folder=folder,
        quality=quality,
        audio_only=audio_only,
        start_time=start_time,
        end_time=end_time,
    )


def _load_config_defaults(
    parse_input: Callable[[str], tuple[list[str], str | None, str | None]],
    default_config_path: str,
) -> tuple[str | None, str | None]:
    try:
        _, folder, quality = parse_input(default_config_path)
        return folder, quality
    except (OSError, ValueError):
        return None, None


def _prompt_url(
    parse_input: Callable[[str], tuple[list[str], str | None, str | None]],
    input_func: Callable[[str], str],
    output_func: Callable[[str], None],
) -> list[str]:
    while True:
        url = input_func("URL: ").strip()
        if not url:
            output_func("URL is required.")
            continue

        if not url.startswith(("http://", "https://")):
            output_func("Invalid URL: use an http:// or https:// URL.")
            continue

        try:
            urls, _, _ = parse_input(url)
            return urls
        except (OSError, ValueError) as exc:
            output_func(f"Invalid URL: {exc}")


def _prompt_folder(default: str, input_func: Callable[[str], str]) -> str:
    value = input_func(f"Download directory [{default}]: ").strip() or default
    expanded = Path(os.path.expandvars(value)).expanduser()
    return str(expanded.resolve())


def _prompt_quality(
    default: str,
    input_func: Callable[[str], str],
    output_func: Callable[[str], None],
) -> str:
    while True:
        quality = input_func(f"Quality [{default}]: ").strip().lower() or default
        if quality in QUALITY_OPTIONS:
            return quality

        output_func(
            "Invalid quality. Use: 144, 240, 360, 480, 720, 1080, or best."
        )


def _prompt_time_range(
    input_func: Callable[[str], str],
    output_func: Callable[[str], None],
) -> tuple[int | float | None, int | float | None]:
    while True:
        start_value = input_func("Start time [from beginning]: ").strip()
        end_value = input_func("End time [until finished]: ").strip()

        try:
            start_time = parse_time_to_seconds(start_value)
            end_time = parse_time_to_seconds(end_value)
            _validate_time_range(start_time, end_time)
            return start_time, end_time
        except ValueError as exc:
            output_func(f"Invalid time range: {exc}")


def _validate_time_range(
    start_time: int | float | None,
    end_time: int | float | None,
) -> None:
    if start_time is not None and start_time < 0:
        raise ValueError("start time must be 0 or greater.")
    if end_time is not None and end_time < 0:
        raise ValueError("end time must be 0 or greater.")
    if start_time is not None and end_time is not None and start_time >= end_time:
        raise ValueError("start time must be less than end time.")


def _format_range(
    start_time: int | float | None,
    end_time: int | float | None,
    audio_only: bool = False,
) -> str:
    if start_time is None and end_time is None:
        return "Full audio" if audio_only else "Full video"

    start = "beginning" if start_time is None else format_duration(start_time)
    end = "finished" if end_time is None else format_duration(end_time)
    return f"{start} - {end}"


def _prompt_yes_no(
    prompt: str,
    default: bool,
    input_func: Callable[[str], str],
    output_func: Callable[[str], None],
) -> bool:
    while True:
        answer = input_func(prompt).strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False

        output_func("Please answer y or n.")
