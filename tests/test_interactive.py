import tempfile
import unittest
from pathlib import Path

from vid_downloader.cli import normalize_command_alias, parse_download_input
from vid_downloader.interactive import collect_interactive_download


def input_from(answers):
    answers = iter(answers)
    return lambda _prompt: next(answers)


class InteractiveDownloadTests(unittest.TestCase):
    def test_download_subcommand_maps_to_non_interactive_flag(self):
        self.assertEqual(
            normalize_command_alias(["download", "https://example.com/video"]),
            ["--download", "https://example.com/video"],
        )

    def test_collects_values_and_confirms_download(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text(
                'URLS=["https://example.com/video"]\n'
                f"DOWNLOAD_DIR={temp_dir}/downloads\n"
                "QUALITY=720\n",
                encoding="utf-8",
            )
            output = []

            result = collect_interactive_download(
                parse_input=parse_download_input,
                input_func=input_from(
                    [str(config_path), "", "", "y", "", "", "yes"]
                ),
                output_func=output.append,
            )

            self.assertIsNotNone(result)
            self.assertEqual(result.urls, ["https://example.com/video"])
            self.assertEqual(
                result.folder,
                str((Path(temp_dir) / "downloads").resolve()),
            )
            self.assertEqual(result.quality, "720")
            self.assertTrue(result.audio_only)
            self.assertIsNone(result.start_time)
            self.assertIsNone(result.end_time)
            self.assertIn("Download summary", output)

    def test_download_can_be_cancelled(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = []

            result = collect_interactive_download(
                parse_input=parse_download_input,
                input_func=input_from(
                    ["https://example.com/video", temp_dir, "", "", "", "", "n"]
                ),
                output_func=output.append,
            )

            self.assertIsNone(result)
            self.assertIn("Download cancelled.", output)

    def test_download_is_confirmed_by_enter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = collect_interactive_download(
                parse_input=parse_download_input,
                input_func=input_from(
                    ["https://example.com/video", temp_dir, "", "", "", "", ""]
                ),
                output_func=lambda _message: None,
            )

            self.assertIsNotNone(result)

    def test_direct_url_uses_directory_default_from_download_config(self):
        def parse_input(value):
            if value == "download.conf":
                return ["https://config.example/video"], "/configured/videos", "720"
            return [value], None, None

        result = collect_interactive_download(
            parse_input=parse_input,
            input_func=input_from(
                ["https://example.com/video", "", "", "n", "", "", ""]
            ),
            output_func=lambda _message: None,
        )

        self.assertEqual(result.folder, "/configured/videos")
        self.assertEqual(result.quality, "720")

    def test_invalid_quality_is_asked_again(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = []

            result = collect_interactive_download(
                parse_input=parse_download_input,
                input_func=input_from(
                    [
                        "https://example.com/video",
                        temp_dir,
                        "4k",
                        "1080",
                        "n",
                        "",
                        "",
                        "y",
                    ]
                ),
                output_func=output.append,
            )

            self.assertEqual(result.quality, "1080")
            self.assertTrue(any("Invalid quality" in line for line in output))

    def test_collects_partial_download_time_range(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = []

            result = collect_interactive_download(
                parse_input=parse_download_input,
                input_func=input_from(
                    [
                        "https://example.com/video",
                        temp_dir,
                        "",
                        "n",
                        "10:12",
                        "13:12",
                        "",
                    ]
                ),
                output_func=output.append,
            )

            self.assertEqual(result.start_time, 612.0)
            self.assertEqual(result.end_time, 792.0)
            self.assertIn("Range     : 10:12 - 13:12", output)

    def test_invalid_time_range_is_asked_again(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = []

            result = collect_interactive_download(
                parse_input=parse_download_input,
                input_func=input_from(
                    [
                        "https://example.com/video",
                        temp_dir,
                        "",
                        "n",
                        "13:12",
                        "10:12",
                        "10:12",
                        "13:12",
                        "",
                    ]
                ),
                output_func=output.append,
            )

            self.assertEqual(result.start_time, 612.0)
            self.assertTrue(any("Invalid time range" in line for line in output))


if __name__ == "__main__":
    unittest.main()
