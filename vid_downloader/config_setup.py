from collections.abc import Callable
from pathlib import Path

from vid_downloader.config_paths import initialize_config


def configure_download_directory(
    config_path: str | Path,
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> Path | None:
    path = Path(config_path).expanduser().resolve()

    if path.exists():
        output_func(f"Configuration already exists: {path}")
        if not _prompt_yes_no(
            "Overwrite it? [y/N]: ",
            default=False,
            input_func=input_func,
            output_func=output_func,
        ):
            output_func("Configuration unchanged.")
            return None
        output_func("")

    output_func("Default download directory")
    output_func("")
    output_func("1. Current directory (where the CLI is started)")
    output_func("2. ~/Downloads")
    output_func("3. Custom directory")

    download_dir = _prompt_download_directory(
        input_func=input_func,
        output_func=output_func,
    )
    return initialize_config(
        path,
        download_dir=download_dir,
        overwrite=path.exists(),
    )


def _prompt_download_directory(
    input_func: Callable[[str], str],
    output_func: Callable[[str], None],
) -> str:
    while True:
        choice = input_func("Select [1]: ").strip()
        if choice in {"", "1"}:
            return ""
        if choice == "2":
            return "~/Downloads"
        if choice == "3":
            custom_dir = input_func("Custom directory: ").strip()
            if custom_dir:
                return custom_dir
            output_func("Directory is required.")
            continue

        output_func("Invalid choice. Select 1, 2, or 3.")


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
