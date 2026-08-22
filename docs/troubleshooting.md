# Troubleshooting

## `uv` is not found

Verify whether uv is available:

```bash
uv --version
```

If it is missing, follow the platform instructions in
[Installation](installation.md#install-uv). After using the standalone
installer, reopen the terminal so its PATH changes are loaded.

## `vdl` or `vid-downloader` is not found

Update the shell PATH and reopen the terminal:

```bash
uv tool update-shell
```

Check installed tools and their executable directory:

```bash
uv tool list
uv tool dir --bin
```

Reinstall from the project directory if necessary:

```bash
uv tool install --force .
```

## The command is still owned by pipx

Remove the old pipx installation once, then install with uv:

```bash
pipx uninstall vid-downloader-cli
uv tool install --force .
uv tool update-shell
```

## Permission denied during installation

Do not run `uv tool install` with `sudo` or an administrator terminal. uv tools
are installed for the current user.

Check whether the command path points to an old installation:

```bash
which vdl
```

On Windows PowerShell:

```powershell
Get-Command vdl
```

## Config is not found

Show the config selected by the CLI:

```bash
vdl config-path
```

Create the global config:

```bash
vdl init
```

Or provide a file explicitly:

```bash
vdl --config /path/to/download.conf
```

See [Configuration](configuration.md) for lookup rules and file syntax.

## Downloads go to an unexpected directory

Check `DOWNLOAD_DIR` in the selected config. If it is empty, the CLI downloads
to the directory where the command was started.

Show the current directory:

```bash
pwd
```

PowerShell equivalent:

```powershell
Get-Location
```

Use `--folder` for an explicit one-time destination.

## Another process is using the download directory

Only one downloader process may write to a destination at a time. Wait for the
other process to finish, or select another directory.

Lock anchors are stored outside downloaded media:

| Platform | Lock directory |
|---|---|
| macOS | `~/Library/Caches/vid-downloader/locks/` |
| Linux | `~/.cache/vid-downloader/locks/` |
| Windows | `%LOCALAPPDATA%\vid-downloader\locks\` |

The files are stable OS-lock anchors and can remain in the cache after a
download finishes.

## Interrupted download does not resume

Run the same download command again. The CLI keeps `.part` files and asks
yt-dlp to continue them. Resume also depends on the source server supporting
range requests.

Do not rename or delete the `.part` file before retrying.

## Browser cookies fail

Close the browser and retry, or select another supported browser:

```bash
vdl download URL --cookies-browser chrome
```

Supported choices are shown by:

```bash
vdl --help
```

## FFmpeg or media merge fails

The project uses `imageio-ffmpeg` to provide an FFmpeg executable. First sync
or reinstall dependencies:

```bash
uv sync
```

For an installed tool:

```bash
uv tool install --force .
```

If the problem continues, run the command again and keep the complete error
message when reporting the issue.

## Run diagnostics from the project

```bash
uv lock --check
uv run python -m unittest discover -s tests -v
uv run vdl --version
```
