import tempfile
import unittest
from pathlib import Path

from vid_downloader.output_naming import (
    build_output_template,
    find_available_output_template,
)


def prepare_filename(info, *, outtmpl):
    return (
        outtmpl.replace("%(title).200s", info["title"])
        .replace("%(id)s", info["id"])
        .replace("%(ext)s", info["ext"])
    )


class OutputNamingTests(unittest.TestCase):
    def test_uses_original_name_when_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            template = find_available_output_template(
                folder=temp_dir,
                filename_mode="title",
                info={"title": "a", "id": "123", "ext": "mp4"},
                prepare_filename=prepare_filename,
                merged_extension="mp4",
            )

            self.assertEqual(template, str(Path(temp_dir) / "%(title).200s.%(ext)s"))

    def test_adds_incrementing_number_when_files_exist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.mp4").touch()
            Path(temp_dir, "a (1).mp4").touch()

            template = find_available_output_template(
                folder=temp_dir,
                filename_mode="title",
                info={"title": "a", "id": "123", "ext": "mp4"},
                prepare_filename=prepare_filename,
                merged_extension="mp4",
            )

            self.assertEqual(
                template,
                str(Path(temp_dir) / "%(title).200s (2).%(ext)s"),
            )

    def test_checks_final_merged_extension(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.mp4").touch()

            template = find_available_output_template(
                folder=temp_dir,
                filename_mode="title",
                info={"title": "a", "id": "123", "ext": "webm"},
                prepare_filename=prepare_filename,
                merged_extension="mp4",
            )

            self.assertEqual(
                template,
                str(Path(temp_dir) / "%(title).200s (1).%(ext)s"),
            )

    def test_part_file_does_not_trigger_copy_number(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            Path(temp_dir, "a.mp4.part").touch()

            template = find_available_output_template(
                folder=temp_dir,
                filename_mode="title",
                info={"title": "a", "id": "123", "ext": "mp4"},
                prepare_filename=prepare_filename,
                merged_extension="mp4",
            )

            self.assertEqual(template, build_output_template(temp_dir, "title"))


if __name__ == "__main__":
    unittest.main()
