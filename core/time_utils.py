def format_duration(seconds: int | float | None) -> str:
    if seconds is None:
        return "Unknown"

    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    return f"{minutes:02d}:{secs:02d}"


def parse_time_to_seconds(value: str | int | float | None) -> int | float | None:
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        pass

    parts = value.split(":")

    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)

    except ValueError:
        pass

    raise ValueError(
        f"Invalid time format: {value}. Use seconds like '90' or timestamp like '00:01:30'."
    )


def resolve_download_range(
    duration: int | float | None,
    start_time: int | float | None = None,
    end_time: int | float | None = None,
) -> tuple[float, float]:
    resolved_start = 0 if start_time is None else float(start_time)

    if resolved_start < 0:
        raise ValueError("start_time must be 0 or greater.")

    if duration is not None:
        resolved_duration = float(duration)

        if resolved_duration <= 0:
            raise ValueError("Video duration is not valid.")

        if resolved_start >= resolved_duration:
            raise ValueError(
                f"start_time cannot be greater than or equal to video duration "
                f"({format_duration(resolved_duration)})."
            )

    if end_time is not None:
        resolved_end = float(end_time)
    elif duration is not None:
        resolved_end = float(duration)
    else:
        raise ValueError(
            "Video duration is not available. Please provide both start_time and end_time for partial download."
        )

    if resolved_end < 0:
        raise ValueError("end_time must be 0 or greater.")

    if resolved_start >= resolved_end:
        raise ValueError("start_time must be less than end_time.")

    if duration is not None:
        resolved_duration = float(duration)

        if resolved_end > resolved_duration:
            print(
                f"Warning: end_time is greater than video duration "
                f"({format_duration(resolved_duration)}). "
                f"Using video duration as end_time."
            )
            resolved_end = resolved_duration

    return resolved_start, resolved_end