import tempfile
import unittest

from core.download_lock import DownloadDirectoryBusyError, DownloadDirectoryLock


class DownloadDirectoryLockTests(unittest.TestCase):
    def test_prevents_two_downloads_in_the_same_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with DownloadDirectoryLock(temp_dir):
                with self.assertRaises(DownloadDirectoryBusyError):
                    with DownloadDirectoryLock(temp_dir):
                        pass

    def test_lock_is_released_after_an_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaisesRegex(RuntimeError, "stopped"):
                with DownloadDirectoryLock(temp_dir):
                    raise RuntimeError("stopped")

            with DownloadDirectoryLock(temp_dir):
                pass


if __name__ == "__main__":
    unittest.main()
