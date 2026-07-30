import ast
import os
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DownloadConfig:
    urls: list[str]
    download_dir: str
    quality: str


def load_download_config(config_path: str) -> DownloadConfig:
    path = Path(config_path).expanduser().resolve()

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"Unable to read config file '{config_path}': {exc}") from exc

    urls_value = _find_value(content, "URLS", allow_multiline=True)
    download_dir_value = _find_value(content, "DOWNLOAD_DIR")
    quality_value = _find_value(content, "QUALITY", required=False)

    urls = _parse_urls(urls_value)
    download_dir = _parse_download_dir(download_dir_value)
    quality = _parse_quality(quality_value)

    if not urls:
        raise ValueError("URLS must contain at least one URL.")

    if not download_dir:
        raise ValueError("DOWNLOAD_DIR must not be empty.")

    expanded_dir = Path(os.path.expandvars(download_dir)).expanduser()
    if not expanded_dir.is_absolute():
        expanded_dir = path.parent / expanded_dir

    return DownloadConfig(
        urls=urls,
        download_dir=str(expanded_dir.resolve()),
        quality=quality,
    )


def _find_value(
    content: str,
    key: str,
    allow_multiline: bool = False,
    required: bool = True,
) -> str:
    if allow_multiline:
        pattern = rf"(?ms)^[ \t]*{key}[ \t]*=[ \t]*(\[[\s\S]*?\])[ \t]*(?:#.*)?$"
    else:
        pattern = rf"(?m)^[ \t]*{key}[ \t]*=[ \t]*(.*?)[ \t]*(?:#.*)?$"

    match = re.search(pattern, content)
    if not match:
        if not required:
            return ""
        raise ValueError(f"Missing {key} in download config.")

    return match.group(1).strip()


def _parse_urls(value: str) -> list[str]:
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        inner_value = value[1:-1]
        parsed = [item.strip() for item in inner_value.split(",")]

    if not isinstance(parsed, (list, tuple)):
        raise ValueError("URLS must be a list.")

    urls = [str(item).strip() for item in parsed if str(item).strip()]
    if any(not url.startswith(("http://", "https://")) for url in urls):
        raise ValueError("Every item in URLS must be an http:// or https:// URL.")

    return urls


def _parse_download_dir(value: str) -> str:
    value = value.strip()
    if not value:
        return ""

    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        parsed = value

    if not isinstance(parsed, str):
        raise ValueError("DOWNLOAD_DIR must be a directory path.")

    return parsed.strip()


def _parse_quality(value: str) -> str:
    quality = value.strip()
    if not quality:
        return "best"

    try:
        parsed = ast.literal_eval(quality)
    except (SyntaxError, ValueError):
        parsed = quality

    quality = str(parsed).strip().lower()
    allowed_qualities = {"144", "240", "360", "480", "720", "1080", "best"}
    if quality not in allowed_qualities:
        allowed = ", ".join(sorted(allowed_qualities))
        raise ValueError(f"Invalid QUALITY '{quality}'. Use one of: {allowed}.")

    return quality
