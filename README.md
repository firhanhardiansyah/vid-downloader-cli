<div align="center">
    <img src="media/logo_large.webp" alt="Vid Downloader CLI Logo"  width="200"/>
    <h1>Vid Downloader CLI</h1>
    <h3><em>Download videos from your terminal—simply, safely, and your way.</em></h3>
</div>

<p align="center">
    <strong>A cross-platform, terminal-first video downloader powered by yt-dlp, with interactive and batch workflows, quality selection, partial downloads, and safe resume support.</strong>
</p>

---

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
```

If `vdl` is not recognized after installation, update the shell `PATH` once and
open a new terminal:

```bash
uv tool update-shell
```

Then start interactive mode:

```bash
vdl
```

On first use, select whether downloads should default to the current directory,
`~/Downloads`, or a custom directory. Reinstalling the CLI keeps this setting.

The full command name is also available:

```bash
vid-downloader
```

## Commands

| Command                                    | Description                                        | Example                                                              |
| ------------------------------------------ | -------------------------------------------------- | -------------------------------------------------------------------- |
| `vdl`                                      | Start the interactive downloader                   | `vdl`                                                                |
| `vdl download`                             | Download every URL from the selected config        | `vdl download`                                                       |
| `vdl download URL`                         | Download one URL without interactive prompts       | `vdl download https://example.com/video`                             |
| `vdl download URL --quality QUALITY`       | Download a video with the selected quality         | `vdl download https://example.com/video --quality 720`               |
| `vdl download URL --audio`                 | Download audio only                                | `vdl download https://example.com/video --audio`                     |
| `vdl download URL --start TIME --end TIME` | Download only the selected time range              | `vdl download https://example.com/video --start 10:12 --end 13:12`   |
| `vdl download URL --folder DIRECTORY`      | Download to a specific directory                   | `vdl download https://example.com/video --folder ~/Downloads/Videos` |
| `vdl download --config PATH`               | Download using a specific config file              | `vdl download --config ~/Downloads/download.conf`                    |
| `vdl init`                                 | Create or reconfigure the global `download.conf`   | `vdl init`                                                           |
| `vdl config-path`                          | Show the config selected for the current directory | `vdl config-path`                                                    |
| `vdl --help`                               | Show all CLI options                               | `vdl --help`                                                         |
| `vdl --version`                            | Show the installed version                         | `vdl --version`                                                      |

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
