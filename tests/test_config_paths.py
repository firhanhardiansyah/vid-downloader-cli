import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from vid_downloader.config_paths import (
    find_default_config_path,
    get_default_download_dir,
    get_global_config_path,
    initialize_config,
)


class ConfigPathsTests(unittest.TestCase):
    def test_default_download_dir_uses_working_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(
                get_default_download_dir(Path(temp_dir)),
                Path(temp_dir).resolve(),
            )

    def test_local_config_has_priority(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            local_config = Path(temp_dir) / "download.conf"
            local_config.touch()

            self.assertEqual(
                find_default_config_path(Path(temp_dir)),
                local_config,
            )

    def test_uses_xdg_global_config_on_unix(self):
        if os.name == "nt":
            self.skipTest("Unix-specific config path")

        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(os.environ, {"XDG_CONFIG_HOME": temp_dir}):
                self.assertEqual(
                    get_global_config_path(),
                    Path(temp_dir) / "vid-downloader" / "download.conf",
                )

    def test_initialize_config_does_not_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config" / "download.conf"

            created_path = initialize_config(config_path)

            self.assertEqual(created_path, config_path.resolve())
            self.assertIn("DOWNLOAD_DIR=", config_path.read_text(encoding="utf-8"))
            with self.assertRaisesRegex(ValueError, "already exists"):
                initialize_config(config_path)

    def test_initialize_config_can_replace_existing_file_explicitly(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "download.conf"
            config_path.write_text("old content", encoding="utf-8")

            initialize_config(
                config_path,
                download_dir="~/Downloads",
                overwrite=True,
            )

            content = config_path.read_text(encoding="utf-8")
            self.assertIn("DOWNLOAD_DIR=~/Downloads", content)
            self.assertNotIn("old content", content)


if __name__ == "__main__":
    unittest.main()
