import os
import sys
from pathlib import Path


DEFAULT_CONFIG_FILENAME = "download.conf"
DEFAULT_CONFIG_TEMPLATE = """\
URLS=[
    "https://example.com/video1",
]

DOWNLOAD_DIR={download_dir}
QUALITY=
"""


def get_default_download_dir(working_directory: Path | None = None) -> Path:
    """Return the directory where the CLI was started."""
    return (working_directory or Path.cwd()).resolve()


def get_global_config_path() -> Path:
    if os.name == "nt":
        config_root = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
    else:
        config_root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

    return config_root / "vid-downloader" / DEFAULT_CONFIG_FILENAME


def get_lock_cache_dir() -> Path:
    if os.name == "nt":
        cache_root = Path(
            os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")
        )
    elif sys.platform == "darwin":
        cache_root = Path.home() / "Library/Caches"
    else:
        cache_root = Path(
            os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")
        )

    return cache_root / "vid-downloader" / "locks"


def find_default_config_path(working_directory: Path | None = None) -> Path:
    current_directory = working_directory or Path.cwd()
    local_config = current_directory / DEFAULT_CONFIG_FILENAME
    if local_config.is_file():
        return local_config

    return get_global_config_path()


def initialize_config(
    config_path: str | Path | None = None,
    download_dir: str = "",
    overwrite: bool = False,
) -> Path:
    path = Path(config_path).expanduser() if config_path else get_global_config_path()
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if overwrite else "x"

    try:
        with path.open(mode, encoding="utf-8") as config_file:
            config_file.write(
                DEFAULT_CONFIG_TEMPLATE.format(download_dir=download_dir)
            )
    except FileExistsError as exc:
        raise ValueError(f"Config file already exists: '{path}'.") from exc
    except OSError as exc:
        raise ValueError(f"Unable to create config file '{path}': {exc}") from exc

    return path
