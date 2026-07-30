# Video Downloader CLI (yt-dlp)

A simple and flexible CLI video downloader built with Python and `yt-dlp`.

This tool supports:

- Downloading the best available video quality
- Downloading a specific resolution (360p, 480p, 720p, 1080p)
- Downloading audio only
- Batch downloading from a `.txt` file
- Simple mode for faster downloads
- Custom output folder selection
- Flexible filename modes
- Optional referer, cookies, and custom headers for protected or embedded sources

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
├── urls.txt
├── urls.example.txt
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

## 4. How to Use

### Prepare a URL List

Create a `urls.txt` file based on the example file:

**Windows**

```bash
copy urls.example.txt urls.txt
```

**Mac / Linux**

```bash
cp urls.example.txt urls.txt
```

Example `urls.txt`:

```txt
https://example.com/video1
https://example.com/video2
https://example.com/video3
```

## 5. Basic Usage

### Download a Single Video

```bash
python main.py https://example.com/video
```

### Download Multiple Videos from a TXT File

```bash
python main.py urls.txt
```

### Download Audio Only

```bash
python main.py https://example.com/video --audio
```

### Download in 720p

```bash
python main.py https://example.com/video --quality 720
```

### Use Simple Mode

```bash
python main.py https://example.com/video --simple
```

## 6. Command-Line Options

| Option                    | Description                                           |
| ------------------------- | ----------------------------------------------------- |
| `input`                   | A video URL or a `.txt` file containing multiple URLs |
| `-q`, `--quality`         | Video quality: `360`, `480`, `720`, `1080`, or `best` |
| `-a`, `--audio`           | Download audio only                                   |
| `-s`, `--simple`          | Enable simple mode for faster downloads               |
| `-v`, `--version`         | Show application version                              |
| `-f`, `--folder`          | Set the output folder                                 |
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

By default, downloaded files are saved to:

```bash
videos/movies
```

You can set a custom output folder using:

```bash
python main.py https://example.com/video --folder downloads
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
python main.py https://example.com/video --filename-mode title_id
```

Use title only:

```bash
python main.py https://example.com/video --filename-mode title
```

Use ID only:

```bash
python main.py https://example.com/video --filename-mode id
```

## 10. Advanced Usage

### Use a Referer Header

Useful for embedded or modal-based video sources:

```bash
python main.py https://example.com/video --referer https://example.com/page
```

### Load Cookies from a Browser

Example using Chrome:

```bash
python main.py https://example.com/video --cookies-browser chrome
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
python main.py https://example.com/video --headers "{\"User-Agent\":\"Mozilla/5.0\"}"
```

Example with multiple headers:

```bash
python main.py https://example.com/video --headers "{\"User-Agent\":\"Mozilla/5.0\",\"X-Test\":\"123\"}"
```

## 11. Example Commands

### Download Best Quality

```bash
python main.py https://example.com/video
```

### Download 720p

```bash
python main.py https://example.com/video --quality 720
```

### Download Audio Only

```bash
python main.py https://example.com/video --audio
```

### Download Using Simple Mode

```bash
python main.py https://example.com/video --simple
```

### Batch Download from TXT

```bash
python main.py urls.txt
```

### Batch Download 720p to a Custom Folder

```bash
python main.py urls.txt --quality 720 --folder downloads
```

### Download Using ID as Filename

```bash
python main.py https://example.com/video --filename-mode id
```

### Download with Browser Cookies and Referer

```bash
python main.py https://example.com/video --referer https://example.com/page --cookies-browser chrome
```

## 12. Running the Project

Each time you want to run the project:

**Windows**

```bash
venv\Scripts\activate
python main.py urls.txt
```

**Mac / Linux**

```bash
source venv/bin/activate
python main.py urls.txt
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
- Batch download from `.txt`
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

Check FFmpeg manually if needed:

```bash
ffmpeg -version
```

## 16. Author

Built with Python and `yt-dlp`.
