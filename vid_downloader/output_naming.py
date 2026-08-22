import os
from collections.abc import Callable
from pathlib import Path


def build_output_template(
    folder: str,
    filename_mode: str,
    copy_number: int = 0,
) -> str:
    templates = {
        "title_id": "%(title).200s [%(id)s]",
        "title": "%(title).200s",
        "id": "%(id)s",
    }

    if filename_mode not in templates:
        raise ValueError(
            "Invalid filename_mode. Use one of: 'title_id', 'title', or 'id'."
        )

    suffix = f" ({copy_number})" if copy_number else ""
    return os.path.join(folder, f"{templates[filename_mode]}{suffix}.%(ext)s")


def find_available_output_template(
    folder: str,
    filename_mode: str,
    info: dict,
    prepare_filename: Callable[..., str],
    merged_extension: str | None = None,
) -> str:
    """Return a numbered template when the final output already exists."""
    copy_number = 0

    while True:
        template = build_output_template(folder, filename_mode, copy_number)
        prepared_path = Path(prepare_filename(info, outtmpl=template))
        possible_outputs = {prepared_path}

        if merged_extension:
            possible_outputs.add(prepared_path.with_suffix(f".{merged_extension}"))

        if not any(path.exists() for path in possible_outputs):
            return template

        copy_number += 1
