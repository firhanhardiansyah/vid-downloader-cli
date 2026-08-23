import unittest
from unittest.mock import patch

from vid_downloader.downloader import MP3_AUDIO_QUALITY, _build_ydl_options


class DownloaderOptionsTests(unittest.TestCase):
    @patch(
        "vid_downloader.downloader.imageio_ffmpeg.get_ffmpeg_exe",
        return_value="/path/to/ffmpeg",
    )
    def test_audio_mode_converts_to_mp3(self, _get_ffmpeg_exe):
        options = _build_ydl_options(
            format_option="bestaudio/best",
            folder="/downloads",
            filename_mode="title",
            http_headers={},
            audio_only=True,
        )

        self.assertNotIn("merge_output_format", options)
        self.assertEqual(
            options["postprocessors"],
            [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": MP3_AUDIO_QUALITY,
                }
            ],
        )

    @patch(
        "vid_downloader.downloader.imageio_ffmpeg.get_ffmpeg_exe",
        return_value="/path/to/ffmpeg",
    )
    def test_video_mode_keeps_mp4_merge(self, _get_ffmpeg_exe):
        options = _build_ydl_options(
            format_option="bestvideo+bestaudio/best",
            folder="/downloads",
            filename_mode="title",
            http_headers={},
            audio_only=False,
        )

        self.assertEqual(options["merge_output_format"], "mp4")
        self.assertNotIn("postprocessors", options)


if __name__ == "__main__":
    unittest.main()
