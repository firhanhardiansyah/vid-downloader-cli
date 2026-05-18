from django.conf import settings
from django.shortcuts import redirect, render

from core.downloader import download_videos
from core.time_utils import parse_time_to_seconds

from .forms import DownloadForm


def index(request):
    result = request.session.pop("download_result", None)
    error = request.session.pop("download_error", None)

    if request.method == "POST":
        form = DownloadForm(request.POST)

        if form.is_valid():
            try:
                urls = form.cleaned_data["input"]
                quality = form.cleaned_data["quality"]
                audio_only = form.cleaned_data["audio"]
                simple = form.cleaned_data["simple"]

                folder_name = form.cleaned_data["folder"]
                folder = settings.ROOT_DIR / folder_name

                filename_mode = form.cleaned_data["filename_mode"]
                referer = form.cleaned_data["referer"] or None
                headers = form.cleaned_data["headers"]
                cookies_browser = form.cleaned_data["cookies_browser"] or None

                start_time = parse_time_to_seconds(form.cleaned_data["start_time"])
                end_time = parse_time_to_seconds(form.cleaned_data["end_time"])

                cookies_from_browser = None
                if cookies_browser:
                    cookies_from_browser = (cookies_browser,)

                download_videos(
                    urls=urls,
                    folder=str(folder),
                    quality=quality,
                    audio_only=audio_only,
                    simple=simple,
                    referer=referer,
                    cookies_from_browser=cookies_from_browser,
                    extra_headers=headers,
                    filename_mode=filename_mode,
                    start_time=start_time,
                    end_time=end_time,
                )

                request.session["download_result"] = {
                    "message": "Download finished successfully.",
                    "total_urls": len(urls),
                    "folder": str(folder),
                }

            except Exception as exc:
                request.session["download_error"] = str(exc)

            return redirect("downloader:index")

    else:
        form = DownloadForm()

    return render(
        request,
        "downloader/index.html",
        {
            "form": form,
            "result": result,
            "error": error,
        },
    )