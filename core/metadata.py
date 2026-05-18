from core.time_utils import format_duration


def print_video_info(
    info: dict,
    index: int | None = None,
    total: int | None = None,
    is_partial_requested: bool = False,
    start_time: int | float | None = None,
    end_time: int | float | None = None,
) -> None:
    title = info.get("title") or "-"
    uploader = info.get("uploader") or info.get("channel") or "-"
    duration = info.get("duration")
    webpage_url = info.get("webpage_url") or info.get("original_url") or "-"
    ext = info.get("ext") or "-"
    resolution = get_selected_resolution(info)
    filesize = get_estimated_filesize(info)

    label = "Video information"
    if index is not None and total is not None:
        label = f"Video information ({index}/{total})"

    print(f"\n{label}")
    print("-" * len(label))
    print(f"Title       : {title}")
    print(f"Uploader    : {uploader}")
    print(f"Duration    : {format_duration(duration)}")
    print(f"Resolution  : {resolution}")
    print(f"Extension   : {ext}")
    print(f"File size   : {format_filesize(filesize)}")
    print(f"URL         : {webpage_url}")

    if is_partial_requested:
        print("")
        print("Partial download")
        print("----------------")
        print(f"Start       : {format_duration(start_time or 0)}")
        print(f"End         : {format_duration(end_time or duration)}")


def get_selected_resolution(info: dict) -> str:
    height = info.get("height")

    if height:
        return f"{height}p"

    requested_formats = info.get("requested_formats") or []

    for item in requested_formats:
        height = item.get("height")

        if height:
            return f"{height}p"

    return "Unknown"


def get_estimated_filesize(info: dict) -> int | None:
    filesize = info.get("filesize") or info.get("filesize_approx")

    if filesize:
        return int(filesize)

    requested_formats = info.get("requested_formats") or []

    if requested_formats:
        total_size = 0

        for item in requested_formats:
            item_size = item.get("filesize") or item.get("filesize_approx")

            if item_size:
                total_size += int(item_size)
                continue

            estimated_size = estimate_size_from_bitrate(item)
            if estimated_size:
                total_size += estimated_size

        return total_size or None

    estimated_size = estimate_size_from_bitrate(info)
    if estimated_size:
        return estimated_size

    return None


def estimate_size_from_bitrate(
    info: dict,
    duration: int | float | None = None,
) -> int | None:
    duration = duration or info.get("duration")
    bitrate = info.get("tbr") or info.get("vbr") or info.get("abr")

    if not duration or not bitrate:
        return None

    return int((float(bitrate) * 1000 / 8) * float(duration))


def format_filesize(size: int | float | None) -> str:
    if not size:
        return "Unknown"

    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"