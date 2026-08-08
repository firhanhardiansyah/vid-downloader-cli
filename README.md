# Vid Downloader CLI

A terminal-first video downloader powered by `yt-dlp`. It supports an
interactive workflow, scriptable commands, partial downloads, resumable
downloads, and an output-directory lock that prevents concurrent writes.

## macOS guide

### Global CLI installation with pipx

Install pipx with Homebrew. Administrator access is not required:

```bash
brew install pipx
pipx ensurepath
```

Open a new terminal, clone the project, and install it:

```bash
git clone <repository-url>
cd vid-downloader-cli
pipx install .
```

Verify both installed commands:

```bash
vid-downloader --version
vdl --version
```

The commands can now be used from any directory. After updating the source,
run this inside the project directory:

```bash
pipx install --force .
```

### Local development with a virtual environment

```bash
git clone <repository-url>
cd vid-downloader-cli

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

Run the downloader using any of these commands:

```bash
python3 main.py download
vid-downloader download
vdl download
```

The CLI commands are available while the virtual environment is active. Exit
the environment with:

```bash
deactivate
```

## Windows guide

The commands below use PowerShell.

### Global CLI installation with pipx

Install pipx for the current user. Administrator access is not required:

```powershell
py -m pip install --user pipx
py -m pipx ensurepath
```

Close and reopen PowerShell so the updated `PATH` is loaded. Then clone and
install the project:

```powershell
git clone <repository-url>
cd vid-downloader-cli
pipx install .
```

Verify both installed commands:

```powershell
vid-downloader --version
vdl --version
```

After updating the source, run this inside the project directory:

```powershell
pipx install --force .
```

### Local development with a virtual environment

```powershell
git clone <repository-url>
cd vid-downloader-cli

py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -e .
```

Run the downloader using any of these commands:

```powershell
py main.py download
vid-downloader download
vdl download
```

The `-e` option installs the project in editable mode, so source changes are
immediately available. Exit the virtual environment with:

```powershell
deactivate
```

## Make commands

On macOS and Linux, the included Makefile provides shortcuts for installation
and development:

```bash
make install      # Install or update the CLI with pipx
make reinstall    # Reinstall the existing pipx package
make uninstall    # Remove the CLI
make test         # Run the unit tests
make dev-install  # Install in editable mode for development
```

`make install` and `make dev-install` run `pipx ensurepath` automatically.
If pipx is unavailable, the Makefile exits without using administrator access
and prints installation guidance for the current environment.

## Interactive usage

Run the command and follow the prompts:

```bash
vid-downloader
```

```text
Video Downloader

URL or config [download.conf]:
Download directory [~/Downloads]:
Quality [best]:
Audio only? [y/N]:
Start time [from beginning]: 10:12
End time [until finished]: 13:12

Download summary
URLs      : 1
Directory : /Users/user/Downloads
Quality   : best
Mode      : Video
Range     : 10:12 - 13:12

Start download? [Y/n]:
```

Press Enter to accept a displayed default. Pressing Enter at the final prompt
starts the download; enter `n` to cancel. `Ctrl+C` cancels cleanly.

## Non-interactive usage

Use the `download` subcommand for scripts and automation:

```bash
vid-downloader download
vid-downloader download https://example.com/video
vid-downloader download https://example.com/video --quality 720
vid-downloader download https://example.com/video --audio
vid-downloader download --folder /path/to/downloads
```

`--download` remains available as a backward-compatible alias.

The legacy command remains available for development compatibility:

```bash
python3 main.py download
```

## Configuration

Create a global config:

```bash
vid-downloader init
```

Show the config selected for the current directory:

```bash
vid-downloader config-path
```

Config lookup order:

1. A file passed with `--config`.
2. `download.conf` in the current directory.
3. The global user config.

Global config locations:

- macOS/Linux: `~/.config/vid-downloader/download.conf`, respecting
  `$XDG_CONFIG_HOME` when set.
- Windows: `%APPDATA%\vid-downloader\download.conf`.

Use a custom config for one run:

```bash
vid-downloader --config /path/to/download.conf
```

Config format:

```ini
URLS=[
    "https://example.com/video1",
    "https://example.com/video2",
]

DOWNLOAD_DIR=~/Downloads
QUALITY=
```

If `DOWNLOAD_DIR` is empty or omitted, it defaults to the current user's
`~/Downloads` directory on macOS, Linux, and Windows. An empty `QUALITY` uses
`best`. Supported values are `144`, `240`, `360`,
`480`, `720`, `1080`, and `best`. Relative download directories are resolved
from the config file's directory.

## Time ranges

Start and end times accept seconds, `MM:SS`, or `HH:MM:SS`:

```bash
vid-downloader download --start 10:12 --end 13:12
```

Leave both values empty in interactive mode to download the full video.

## Options

```text
--download                 Run without interactive prompts
--config PATH              Use a specific config file
-q, --quality QUALITY      Override config quality
-a, --audio                Download audio only
-s, --simple               Use the simple yt-dlp format
-f, --folder PATH          Override the download directory
--filename-mode MODE       title (default), title_id, or id
-r, --referer URL          Send a Referer header
-c, --cookies-browser NAME Load cookies from a browser
--headers JSON             Send additional HTTP headers
--start TIME               Partial-download start time
--end TIME                 Partial-download end time
-v, --version              Print the version
```

Run `vid-downloader --help` for the complete generated help.

## Resume and concurrency safety

Interrupted downloads retain their `.part` file. Run the same command again to
resume when the source server supports range requests. Temporary fragments are
removed after a successful download.

Only one process may use a `DOWNLOAD_DIR` at a time. Lock anchors are stored
outside the download directory in the user's cache, using a hash of the output
path as the filename:

- macOS: `~/Library/Caches/vid-downloader/locks/`
- Linux: `~/.cache/vid-downloader/locks/`
- Windows: `%LOCALAPPDATA%\vid-downloader\locks\`

The cache lock files contain no media data and remain as stable OS-lock anchors
to avoid inode race conditions. Legacy `.vid-downloader.lock` files in download
folders can be removed after confirming no older downloader process is running.

## Test

```bash
python -m unittest discover -s tests -v
```
