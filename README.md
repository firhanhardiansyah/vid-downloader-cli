# Video Downloader CLI (yt-dlp)

A simple and flexible CLI video downloader built with Python and `yt-dlp`.

This tool supports:

- Downloading the best available video quality
- Downloading a specific resolution (360p, 480p, 720p, 1080p)
- Downloading audio only
- Batch downloading from a single download config
- Simple mode for faster downloads
- Custom output folder selection
- Flexible filename modes
- Optional referer, cookies, and custom headers for protected or embedded sources
- Safe resume from `.part` files after an interrupted download
- Output-directory locking to prevent concurrent writes and race conditions

## 1. Project Setup

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Mac / Linux**

```bash
source .venv/bin/activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

## 2. Requirements

Create a `requirements.txt` file:

```txt
yt-dlp
imageio-ffmpeg
```

## 3. Project Structure

```bash
video_downloader/
│
├── core/
│   ├── downloader.py
│   └── utils.py
│
├── videos/
├── download.conf
├── download.example.conf
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

## 4. How to Use

### Prepare the Download Config

Create a private `download.conf` file based on the example:

**Windows**

```bash
copy download.example.conf download.conf
```

**Mac / Linux**

```bash
cp download.example.conf download.conf
```

Example `download.conf`:

```ini
URLS=[
    "https://example.com/video1",
    "https://example.com/video2",
    "https://example.com/video3",
]

DOWNLOAD_DIR=~/Downloads/videos

# Empty means best quality.
QUALITY=
```

`DOWNLOAD_DIR` may be an absolute path outside this project, a path starting
with `~`, or a relative path. Relative paths are resolved from the directory
containing `download.conf`.

## 5. Basic Usage

### Interactive Mode

Run the CLI without arguments and follow the prompts:

```bash
python main.py
```

```text
Video Downloader

URL or config [download.conf]:
Download directory [~/Downloads/videos]:
Quality [best]:
Audio only? [y/N]:
Start time [from beginning]: 10:12
End time [until finished]: 13:12

Download summary
URLs      : 3
Directory : /Users/your-name/Downloads/videos
Quality   : best
Mode      : Video
Range     : 10:12 - 13:12

Start download? [Y/n]:
```

Press Enter to use each displayed default. `DOWNLOAD_DIR` and `QUALITY` default
to the values in `download.conf`, even when entering a URL directly. The final
confirmation defaults to `Yes`, so pressing Enter starts the download. Use
`Ctrl+C` at any prompt to cancel cleanly.

Time values accept seconds, `MM:SS`, or `HH:MM:SS`. Leave both time prompts
empty to download the full video. For example, `10:12` through `13:12`
downloads a three-minute segment.

### Non-interactive Mode

Use `--download` for scripts or to start immediately from `download.conf`:

```bash
python main.py --download
```

### Download a Single Video

```bash
python main.py --download https://example.com/video
```

### Download Everything in the Config

```bash
python main.py --download
```

You can also provide a config file explicitly:

```bash
python main.py --download /path/to/my-download.conf
```

### Download Audio Only

```bash
python main.py --download https://example.com/video --audio
```

### Download in 720p

```bash
python main.py --download https://example.com/video --quality 720
```

### Use Simple Mode

```bash
python main.py --download https://example.com/video --simple
```

## 6. Command-Line Options

| Option                    | Description                                           |
| ------------------------- | ----------------------------------------------------- |
| `--download`              | Start the download process                            |
| `input`                   | A video URL or config file (defaults to `download.conf`) |
| `-q`, `--quality`         | Video quality: `360`, `480`, `720`, `1080`, or `best` |
| `-a`, `--audio`           | Download audio only                                   |
| `-s`, `--simple`          | Enable simple mode for faster downloads               |
| `-v`, `--version`         | Show application version                              |
| `-f`, `--folder`          | Override `DOWNLOAD_DIR` from the config               |
| `--filename-mode`         | Set filename format: `title_id`, `title`, or `id`     |
| `-r`, `--referer`         | Set a referer URL for embedded or protected media     |
| `-c`, `--cookies-browser` | Load cookies from a browser session                   |
| `--headers`               | Pass extra HTTP headers as a JSON object              |

## 7. Download Modes

| Mode                       | Format                                | Description                                        |
| -------------------------- | ------------------------------------- | -------------------------------------------------- |
| Best                       | `bestvideo+bestaudio/best`            | Best available quality with merged video and audio |
| 360p / 480p / 720p / 1080p | `bestvideo[height<=X]+bestaudio/best` | Download a specific resolution                     |
| Audio                      | `bestaudio/best`                      | Download audio only                                |
| Simple                     | `best`                                | Faster download using a simpler format             |

## 8. Output Folder

Set the output directory in `download.conf`. It can be outside the project:

```ini
DOWNLOAD_DIR=/Users/your-name/Downloads/videos
```

For a one-off override, use `--folder`:

```bash
python main.py --download --folder /another/output/directory
```

## 9. Filename Modes

The downloader supports multiple filename formats.

### Available Modes

| Mode       | Example Output                |
| ---------- | ----------------------------- |
| `title_id` | `My Video Title [abc123].mp4` |
| `title`    | `My Video Title.mp4`          |
| `id`       | `abc123.mp4`                  |

### Example Usage

Use title + ID:

```bash
python main.py --download https://example.com/video --filename-mode title_id
```

Use title only:

```bash
python main.py --download https://example.com/video --filename-mode title
```

Use ID only:

```bash
python main.py --download https://example.com/video --filename-mode id
```

## 10. Advanced Usage

### Use a Referer Header

Useful for embedded or modal-based video sources:

```bash
python main.py --download https://example.com/video --referer https://example.com/page
```

### Load Cookies from a Browser

Example using Chrome:

```bash
python main.py --download https://example.com/video --cookies-browser chrome
```

Supported browsers:

- `chrome`
- `firefox`
- `edge`
- `brave`
- `opera`
- `chromium`
- `safari`

### Send Extra Headers

```bash
python main.py --download https://example.com/video --headers "{\"User-Agent\":\"Mozilla/5.0\"}"
```

Example with multiple headers:

```bash
python main.py --download https://example.com/video --headers "{\"User-Agent\":\"Mozilla/5.0\",\"X-Test\":\"123\"}"
```

## 11. Example Commands

### Download Best Quality

```bash
python main.py --download https://example.com/video
```

### Download 720p

```bash
python main.py --download https://example.com/video --quality 720
```

### Download Audio Only

```bash
python main.py --download https://example.com/video --audio
```

### Download Using Simple Mode

```bash
python main.py --download https://example.com/video --simple
```

### Batch Download from Config

```bash
python main.py --download
```

### Batch Download 720p to a Custom Folder

```bash
python main.py --download --quality 720 --folder /path/to/downloads
```

### Download Using ID as Filename

```bash
python main.py --download https://example.com/video --filename-mode id
```

### Download with Browser Cookies and Referer

```bash
python main.py --download https://example.com/video --referer https://example.com/page --cookies-browser chrome
```

## 12. Running the Project

Each time you want to run the project:

**Windows**

```bash
venv\Scripts\activate
python main.py --download
```

**Mac / Linux**

```bash
source venv/bin/activate
python main.py --download
```

## 13. .gitignore

```gitignore
venv/
__pycache__/
videos/
*.mp4
*.mp3
```

## 14. Features

- Video download
- Audio-only download
- Batch download from `download.conf`
- Quality selection
- Simple mode
- Custom output folder
- Flexible filename modes
- Referer support
- Browser cookie support
- Custom HTTP headers
- CLI-based workflow

## 15. Notes

- If you download high-quality video where video and audio are separate streams, **FFmpeg is required**.
- This project uses `imageio-ffmpeg` to provide FFmpeg automatically in Python environments.
- Some websites may require a referer, cookies, or custom headers to allow media downloads.
- If multiple videos have the same title, using `title_id` or `id` is recommended to avoid filename conflicts.
- If a download is interrupted, run `python main.py --download` again. The downloader
  will reuse the existing `.part` file when the source server supports resuming.
- Temporary fragments are removed after a successful download. An unfinished
  `.part` file is intentionally retained so the next run can resume it.
- Only one downloader process may use the same `DOWNLOAD_DIR` at a time. A second
  process exits safely instead of writing to the same files concurrently.
- `.vid-downloader.lock` is a small persistent lock anchor, not download data.
  It is intentionally retained because deleting an OS lock file can introduce
  an inode race between downloader processes.

Check FFmpeg manually if needed:

```bash
ffmpeg -version
```

## 16. Author

Built with Python and `yt-dlp`.
