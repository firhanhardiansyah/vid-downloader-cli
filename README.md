# Vid Downloader CLI

A terminal-first video downloader powered by `yt-dlp`. Download interactively,
run batches from a config file, select video quality, download a time range,
and safely resume interrupted downloads.

## Features

- Interactive and non-interactive workflows
- Batch URLs through `download.conf`
- Video quality and audio-only modes
- Partial downloads using start and end times
- Resume support through `.part` files
- Automatic duplicate names such as `video (1).mp4`
- Cross-process locking without adding lock files to the output directory
- macOS, Linux, and Windows support

## Get started

[Install uv](docs/installation.md#install-uv), then clone and install the CLI:

```bash
git clone https://github.com/firhanhardiansyah/vid-downloader-cli.git
cd vid-downloader-cli
uv tool install .
uv tool update-shell
```

Open a new terminal after the first installation, then start interactive mode:

```bash
vdl
```

The full command name is also available:

```bash
vid-downloader
```

## Commands

| Command | Example | Description |
|---|---|---|
| `vdl` | `vdl` | Start the interactive downloader |
| `vdl download` | `vdl download` | Download every URL from the selected config |
| `vdl download URL` | `vdl download https://example.com/video` | Download one URL without interactive prompts |
| `vdl download URL --quality QUALITY` | `vdl download https://example.com/video --quality 720` | Download a video with the selected quality |
| `vdl download URL --audio` | `vdl download https://example.com/video --audio` | Download audio only |
| `vdl download URL --start TIME --end TIME` | `vdl download https://example.com/video --start 10:12 --end 13:12` | Download only the selected time range |
| `vdl download URL --folder DIRECTORY` | `vdl download https://example.com/video --folder ~/Downloads/Videos` | Download to a specific directory |
| `vdl download --config PATH` | `vdl download --config ~/Downloads/download.conf` | Download using a specific config file |
| `vdl init` | `vdl init` | Create the global `download.conf` |
| `vdl config-path` | `vdl config-path` | Show the config selected for the current directory |
| `vdl --help` | `vdl --help` | Show all CLI options |
| `vdl --version` | `vdl --version` | Show the installed version |

## Quick configuration

Create `download.conf` in the directory where the command will run:

```ini
URLS=[
    "https://example.com/video1",
    "https://example.com/video2",
]

# Empty means the current working directory.
DOWNLOAD_DIR=

# Empty means best quality.
QUALITY=
```

Run the batch:

```bash
vdl download
```

Interactive mode asks for a direct URL. It uses `DOWNLOAD_DIR` and `QUALITY`
from the selected config as defaults, but does not read `URLS` from it.

## Update or remove

From the cloned project directory:

```bash
uv tool install --force .       # Update/reinstall
uv tool uninstall vid-downloader-cli
```

If GNU Make is installed, equivalent shortcuts are available:

```bash
make install
make reinstall
make uninstall
make test
make dev-install
make sync
```

## Documentation

- [Installation](docs/installation.md) — uv setup for macOS, Linux, and Windows
- [Configuration](docs/configuration.md) — config lookup, options, and batch URLs
- [Development](docs/development.md) — uv workflow, tests, and project structure
- [Troubleshooting](docs/troubleshooting.md) — PATH, permissions, resume, and locks
