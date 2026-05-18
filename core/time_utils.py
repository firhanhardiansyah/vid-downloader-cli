def format_duration(seconds: int | float | None) -> str:
    if seconds is None:
        return "Unknown"

    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    return f"{minutes:02d}:{secs:02d}"


def resolve_download_range(
    duration: int | float | None,
    start_time: int | float | None = None,
    end_time: int | float | None = None,
) -> tuple[int | float, int | float]:
    if duration is None:
        raise ValueError(
            "Video duration is not available, so partial download cannot be resolved safely."
        )

    resolved_start = 0 if start_time is None else start_time
    resolved_end = duration if end_time is None else end_time

    if resolved_start < 0:
        raise ValueError("start_time must be 0 or greater.")

    if resolved_end < 0:
        raise ValueError("end_time must be 0 or greater.")

    if resolved_start >= resolved_end:
        raise ValueError("start_time must be less than end_time.")

    return resolved_start, resolved_end


def parse_time_to_seconds(value: str | int | float | None) -> int | None:
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    if value.isdigit():
        return int(value)

    parts = value.split(":")

    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)

    except ValueError:
        pass

    raise ValueError(
        f"Invalid time format: {value}. Use seconds like '90' or timestamp like '00:01:30'."
    )


def format_duration(seconds: int | float | None) -> str:
    if seconds is None:
        return "Unknown"

    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    return f"{minutes:02d}:{secs:02d}"


def resolve_download_range(
    duration: int | float | None,
    start_time: int | float | None = None,
    end_time: int | float | None = None,
) -> tuple[int | float, int | float]:
    if duration is None:
        raise ValueError(
            "Video duration is not available, so partial download cannot be resolved safely."
        )

    resolved_start = 0 if start_time is None else start_time
    resolved_end = duration if end_time is None else end_time

    if resolved_start < 0:
        raise ValueError("start_time must be 0 or greater.")

    if resolved_end < 0:
        raise ValueError("end_time must be 0 or greater.")

    if resolved_start >= resolved_end:
        raise ValueError("start_time must be less than end_time.")

    return resolved_start, resolved_end