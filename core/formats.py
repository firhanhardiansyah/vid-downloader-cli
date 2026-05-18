def build_format_option(
    quality: str,
    audio_only: bool = False,
    simple: bool = False,
    is_partial_requested: bool = False,
) -> str:
    quality = validate_quality(quality)

    if audio_only:
        return "bestaudio/best"

    if simple:
        if quality == "best":
            return "best"

        return (
            f"best[height<={quality}][ext=mp4]/"
            f"best[height<={quality}]"
        )

    if is_partial_requested:
        if quality == "best":
            return "best[ext=mp4]/best"

        return (
            f"best[height<={quality}][ext=mp4]/"
            f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/"
            f"bestvideo[height<={quality}]+bestaudio/"
            f"best[height<={quality}]"
        )

    if quality == "best":
        return "bestvideo+bestaudio/best"

    return (
        f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/"
        f"bestvideo[height<={quality}]+bestaudio/"
        f"best[height<={quality}][ext=mp4]/"
        f"best[height<={quality}]"
    )


def validate_quality(quality: str) -> str:
    allowed_qualities = {"144", "240", "360", "480", "720", "1080", "best"}

    quality = str(quality).strip().lower()

    if quality not in allowed_qualities:
        raise ValueError(
            "Invalid quality. Use one of: 144, 240, 360, 480, 720, 1080, or best."
        )

    return quality