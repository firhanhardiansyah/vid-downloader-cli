# Installation

Vid Downloader uses [uv](https://docs.astral.sh/uv/) to install the CLI in an
isolated environment. Do not use `sudo` when installing this project.

## Requirements

- Git
- uv
- An internet connection during installation

uv can install and select a compatible Python runtime when needed. The project
requires Python 3.10 or newer.

## Install uv

### macOS

With Homebrew:

```bash
brew install uv
```

Or use the official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Linux

Use the official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

In PowerShell, use WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Or use the official standalone installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify the installation:

```bash
uv --version
```

## Install Vid Downloader

These commands work in macOS, Linux, and Windows terminals:

```bash
git clone https://github.com/firhanhardiansyah/vid-downloader-cli.git
cd vid-downloader-cli
uv tool install .
uv tool update-shell
```

Close and reopen the terminal after `uv tool update-shell`, then verify:

```bash
vdl --version
vid-downloader --version
```

Both names run the same CLI.

Run the CLI once to complete the initial setup:

```bash
vdl
```

If no global config exists, choose a default download directory:

```text
Default download directory

1. Current directory (where the CLI is started)
2. ~/Downloads
3. Custom directory
Select [1]:
```

Press Enter to use the directory where `vdl` is started. The selection is
stored in the global `download.conf` and is only requested once.

## Install with Make

If GNU Make is available:

```bash
make install
```

This installs the tool and updates the shell PATH through uv. Make is commonly
available on macOS and Linux, but is not included with Windows by default.

## Update or reinstall

Pull the latest source and reinstall it:

```bash
git pull
uv tool install --force .
```

With Make:

```bash
git pull
make reinstall
```

Reinstalling replaces the CLI environment but does not remove or recreate the
global `download.conf`. The existing download-directory setting remains in
effect. Run `vdl init` only when you want to change it.

## Editable tool installation

For a globally available command that follows source-code changes:

```bash
uv tool install --force --editable .
uv tool update-shell
```

For regular project development, prefer `uv sync` and `uv run`; see
[Development](development.md).

## Uninstall

```bash
uv tool uninstall vid-downloader-cli
```

Or:

```bash
make uninstall
```

Downloaded media and user config files are not removed.

## Migrating from pipx

If an older version was installed with pipx, remove it before using uv so the
two managers do not own the same command:

```bash
pipx uninstall vid-downloader-cli
uv tool install .
uv tool update-shell
```

See [Troubleshooting](troubleshooting.md) if `vdl` is not found after setup.
