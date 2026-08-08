import tempfile
import unittest
from pathlib import Path

from vid_downloader.download_config import load_download_config


class DownloadConfigTests(unittest.TestCase):
    def test_loads_urls_and_resolves_relative_download_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text(
                'URLS=["https://example.com/one", "https://example.com/two"]\n'
                "DOWNLOAD_DIR=../media\n",
                encoding="utf-8",
            )

            config = load_download_config(str(config_path))

            self.assertEqual(
                config.urls,
                ["https://example.com/one", "https://example.com/two"],
            )
            self.assertEqual(
                config.download_dir,
                str((Path(temp_dir) / "../media").resolve()),
            )
            self.assertEqual(config.quality, "best")

    def test_accepts_unquoted_urls_and_absolute_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "outside" / "videos"
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text(
                "URLS=[https://example.com/one, https://example.com/two]\n"
                f"DOWNLOAD_DIR={output_dir}\n"
                "QUALITY=720\n",
                encoding="utf-8",
            )

            config = load_download_config(str(config_path))

            self.assertEqual(len(config.urls), 2)
            self.assertEqual(config.download_dir, str(output_dir.resolve()))
            self.assertEqual(config.quality, "720")

    def test_empty_download_directory_uses_working_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text(
                'URLS=["https://example.com/one"]\nDOWNLOAD_DIR=\n',
                encoding="utf-8",
            )

            config = load_download_config(str(config_path))

            self.assertEqual(
                config.download_dir,
                str(Path.cwd().resolve()),
            )

    def test_missing_download_directory_uses_working_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text(
                'URLS=["https://example.com/one"]\n',
                encoding="utf-8",
            )

            config = load_download_config(str(config_path))

            self.assertEqual(
                config.download_dir,
                str(Path.cwd().resolve()),
            )

    def test_rejects_invalid_quality(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text(
                'URLS=["https://example.com/one"]\n'
                "DOWNLOAD_DIR=videos\n"
                "QUALITY=4k\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Invalid QUALITY"):
                load_download_config(str(config_path))


if __name__ == "__main__":
    unittest.main()
