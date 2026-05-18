import json

from django import forms


class DownloadForm(forms.Form):
    input = forms.CharField(
        label="Video URL or URL list",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "placeholder": "Paste video URL here. For multiple URLs, use one URL per line.",
            }
        ),
    )

    quality = forms.ChoiceField(
        label="Quality",
        choices=[
            ("best", "Best"),
            ("1080", "1080p"),
            ("720", "720p"),
            ("480", "480p"),
            ("360", "360p"),
            ("240", "240p"),
            ("144", "144p"),
        ],
        initial="best",
    )

    audio = forms.BooleanField(
        label="Download audio only",
        required=False,
    )

    simple = forms.BooleanField(
        label="Simple mode",
        required=False,
    )

    folder = forms.CharField(
        label="Output folder",
        initial="videos",
        required=True,
    )

    filename_mode = forms.ChoiceField(
        label="Filename mode",
        choices=[
            ("title_id", "Title + ID"),
            ("title", "Title only"),
            ("id", "ID only"),
        ],
        initial="title_id",
    )

    referer = forms.URLField(
        label="Referer URL",
        required=False,
        widget=forms.URLInput(
            attrs={
                "placeholder": "https://example.com",
            }
        ),
    )

    cookies_browser = forms.ChoiceField(
        label="Cookies from browser",
        required=False,
        choices=[
            ("", "None"),
            ("chrome", "Chrome"),
            ("firefox", "Firefox"),
            ("edge", "Edge"),
            ("brave", "Brave"),
            ("opera", "Opera"),
            ("chromium", "Chromium"),
            ("safari", "Safari"),
        ],
    )

    headers = forms.CharField(
        label="Extra HTTP headers",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": '{"User-Agent": "Mozilla/5.0"}',
            }
        ),
    )

    start_time = forms.CharField(
        label="Start time",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "00:01:30 or 90",
            }
        ),
    )

    end_time = forms.CharField(
        label="End time",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "00:03:00 or 180",
            }
        ),
    )

    def clean_headers(self):
        headers = self.cleaned_data.get("headers")

        if not headers:
            return None

        try:
            parsed_headers = json.loads(headers)
        except json.JSONDecodeError as exc:
            raise forms.ValidationError(f"Invalid JSON headers: {exc}") from exc

        if not isinstance(parsed_headers, dict):
            raise forms.ValidationError("Headers must be a JSON object.")

        return parsed_headers

    def clean_input(self):
        value = self.cleaned_data["input"]

        urls = [line.strip() for line in value.splitlines() if line.strip()]

        if not urls:
            raise forms.ValidationError("Please provide at least one video URL.")

        return urls