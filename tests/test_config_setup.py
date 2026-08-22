import tempfile
import unittest
from pathlib import Path

from vid_downloader.config_setup import configure_download_directory


def input_from(answers):
    answers = iter(answers)
    return lambda _prompt: next(answers)


class ConfigSetupTests(unittest.TestCase):
    def test_enter_selects_current_working_directory_behavior(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"

            result = configure_download_directory(
                config_path,
                input_func=input_from([""]),
                output_func=lambda _message: None,
            )

            self.assertEqual(result, config_path.resolve())
            self.assertIn(
                "DOWNLOAD_DIR=\n",
                config_path.read_text(encoding="utf-8"),
            )

    def test_downloads_option_uses_portable_home_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"

            configure_download_directory(
                config_path,
                input_func=input_from(["2"]),
                output_func=lambda _message: None,
            )

            self.assertIn(
                "DOWNLOAD_DIR=~/Downloads",
                config_path.read_text(encoding="utf-8"),
            )

    def test_custom_directory_is_saved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"

            configure_download_directory(
                config_path,
                input_func=input_from(["3", "~/Videos"]),
                output_func=lambda _message: None,
            )

            self.assertIn(
                "DOWNLOAD_DIR=~/Videos",
                config_path.read_text(encoding="utf-8"),
            )

    def test_existing_config_is_unchanged_by_default(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text("existing config", encoding="utf-8")
            output = []

            result = configure_download_directory(
                config_path,
                input_func=input_from([""]),
                output_func=output.append,
            )

            self.assertIsNone(result)
            self.assertEqual(
                config_path.read_text(encoding="utf-8"),
                "existing config",
            )
            self.assertIn("Configuration unchanged.", output)

    def test_existing_config_can_be_reconfigured(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text("existing config", encoding="utf-8")

            result = configure_download_directory(
                config_path,
                input_func=input_from(["y", "2"]),
                output_func=lambda _message: None,
            )

            self.assertEqual(result, config_path.resolve())
            self.assertIn(
                "DOWNLOAD_DIR=~/Downloads",
                config_path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
