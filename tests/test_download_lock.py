import tempfile
import unittest
from pathlib import Path

from vid_downloader.download_lock import (
    DownloadDirectoryBusyError,
    DownloadDirectoryLock,
)


class DownloadDirectoryLockTests(unittest.TestCase):
    def test_prevents_two_downloads_in_the_same_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            lock_dir = Path(temp_dir) / "cache"

            with DownloadDirectoryLock(output_dir, lock_dir):
                with self.assertRaises(DownloadDirectoryBusyError):
                    with DownloadDirectoryLock(output_dir, lock_dir):
                        pass

    def test_lock_is_released_after_an_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            lock_dir = Path(temp_dir) / "cache"

            with self.assertRaisesRegex(RuntimeError, "stopped"):
                with DownloadDirectoryLock(output_dir, lock_dir):
                    raise RuntimeError("stopped")

            with DownloadDirectoryLock(output_dir, lock_dir):
                pass

    def test_lock_is_stored_in_cache_not_download_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output"
            lock_dir = Path(temp_dir) / "cache"

            lock = DownloadDirectoryLock(output_dir, lock_dir)
            with lock:
                self.assertEqual(lock.lock_path.parent, lock_dir.resolve())
                self.assertTrue(lock.lock_path.is_file())

            self.assertFalse((output_dir / ".vid-downloader.lock").exists())

    def test_different_directories_use_different_lock_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            lock_dir = Path(temp_dir) / "cache"
            first = DownloadDirectoryLock(Path(temp_dir) / "one", lock_dir)
            second = DownloadDirectoryLock(Path(temp_dir) / "two", lock_dir)

            self.assertNotEqual(first.lock_path, second.lock_path)


if __name__ == "__main__":
    unittest.main()
