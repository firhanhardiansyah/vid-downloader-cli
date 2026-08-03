import os
from importlib import import_module
from pathlib import Path
from typing import Any, TextIO


LOCK_FILENAME = ".vid-downloader.lock"
_LOCK_API: Any = import_module("msvcrt" if os.name == "nt" else "fcntl")


class DownloadDirectoryBusyError(RuntimeError):
    """Raised when another process is downloading to the same directory."""


def _acquire_file_lock(lock_file: TextIO) -> None:
    if hasattr(_LOCK_API, "locking"):
        lock_file.seek(0, os.SEEK_END)
        if lock_file.tell() == 0:
            lock_file.write("\0")
            lock_file.flush()

        lock_file.seek(0)
        _LOCK_API.locking(lock_file.fileno(), _LOCK_API.LK_NBLCK, 1)
        return

    _LOCK_API.flock(
        lock_file.fileno(),
        _LOCK_API.LOCK_EX | _LOCK_API.LOCK_NB,
    )


def _release_file_lock(lock_file: TextIO) -> None:
    if hasattr(_LOCK_API, "locking"):
        lock_file.seek(0)
        _LOCK_API.locking(lock_file.fileno(), _LOCK_API.LK_UNLCK, 1)
        return

    _LOCK_API.flock(lock_file.fileno(), _LOCK_API.LOCK_UN)


def _write_lock_owner(lock_file: TextIO) -> None:
    lock_file.seek(0)
    lock_file.truncate()
    lock_file.write(f"pid={os.getpid()}\n")
    lock_file.flush()


class DownloadDirectoryLock:
    """Prevent concurrent downloader processes from sharing an output folder."""

    def __init__(self, folder: str):
        self.lock_path = Path(folder) / LOCK_FILENAME
        self._lock_file: TextIO | None = None

    def __enter__(self):
        lock_file = self.lock_path.open("a+", encoding="utf-8")
        self._lock_file = lock_file

        try:
            _acquire_file_lock(lock_file)
        except OSError as exc:
            lock_file.close()
            self._lock_file = None
            raise DownloadDirectoryBusyError(
                "Another download process is already using "
                f"'{self.lock_path.parent}'. Wait for it to finish, then retry."
            ) from exc

        _write_lock_owner(lock_file)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        lock_file = self._lock_file
        if lock_file is None:
            return

        try:
            _release_file_lock(lock_file)
        finally:
            lock_file.close()
            self._lock_file = None
