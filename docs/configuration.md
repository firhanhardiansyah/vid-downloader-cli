# Configuration

## Config format

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

Copy the provided example when creating a project-local config:

```bash
cp download.example.conf download.conf
```

On Windows PowerShell:

```powershell
Copy-Item download.example.conf download.conf
```

`download.conf` is ignored by Git because it may contain private URLs.

## Config lookup order

The CLI selects config in this order:

1. A file explicitly passed with `--config`.
2. `download.conf` in the current working directory.
3. The global user config.

Show the selected path:

```bash
vdl config-path
```

Use a specific file:

```bash
vdl --config /path/to/download.conf
```

## Global config

Create or reconfigure it with:

```bash
vdl init
```

The setup asks whether downloads should default to the current directory,
`~/Downloads`, or a custom directory. If the config already exists, it shows
the selected path and asks before overwriting it:

```text
Configuration already exists: /path/to/download.conf
Overwrite it? [y/N]:
```

Press Enter to keep the existing config unchanged. The same setup runs
automatically the first time `vdl` is started without a local or global config.

Default locations:

| Platform | Location |
|---|---|
| macOS/Linux | `~/.config/vid-downloader/download.conf` |
| Windows | `%APPDATA%\vid-downloader\download.conf` |

macOS/Linux respects `$XDG_CONFIG_HOME` when it is set.

## URLs

`URLS` is used by non-interactive batch mode:

```bash
vdl download
```

URLs run sequentially in the listed order. Interactive mode always asks for a
direct HTTP/HTTPS URL and does not read `URLS`.

## Download directory

If `DOWNLOAD_DIR` is empty or missing, the current working directory is used:

```ini
DOWNLOAD_DIR=
```

Use a portable home-relative path on macOS, Linux, and Windows:

```ini
DOWNLOAD_DIR=~/Downloads/Videos
```

Relative paths are resolved from the directory containing the config file:

```ini
DOWNLOAD_DIR=downloads
```

Override it for one command:

```bash
vdl download URL --folder /another/directory
```

Priority is `--folder`, non-empty `DOWNLOAD_DIR`, then current working
directory.

## Quality

Supported values:

```text
144
240
360
480
720
1080
best
```

An empty value uses `best`:

```ini
QUALITY=
```

Override it for one command:

```bash
vdl download URL --quality 720
```

## Audio-only MP3

Use `--audio` to download the best available audio stream and convert it to
MP3 at 192 kbps:

```bash
vdl download URL --audio
```

Video `QUALITY` is ignored in audio mode. Interactive mode provides the same
behavior through `Audio only (MP3)? [y/N]`.

## Time ranges

Accepted formats are seconds, `MM:SS`, and `HH:MM:SS`:

```bash
vdl download URL --start 10:12 --end 13:12
```

The start time must be lower than the end time. Leave both empty in
interactive mode to download the full video.

## Filename modes

| Mode | Example |
|---|---|
| `title` | `My Video.mp4` |
| `title_id` | `My Video [abc123].mp4` |
| `id` | `abc123.mp4` |

`title` is the default:

```bash
vdl download URL --filename-mode title_id
```

If the target already exists, the CLI creates `My Video (1).mp4`, then
`My Video (2).mp4`, and so on. A `.part` file is kept for resume and does not
trigger a new number.

## Advanced request options

Load cookies from a supported browser:

```bash
vdl download URL --cookies-browser chrome
```

Set a Referer header:

```bash
vdl download URL --referer https://example.com/page
```

Send additional headers as JSON:

```bash
vdl download URL --headers '{"User-Agent":"Mozilla/5.0"}'
```

Run `vdl --help` for the complete option list.
