# Video Downloader CLI (yt-dlp)

A simple CLI Video Downloader built with Python and yt-dlp.

This tool can:

- Download best quality video
- Download specific resolution (360p, 480p, 720p, 1080p)
- Download audio only
- Batch download from `.txt` file
- Simple mode (fast download without selecting quality)

---

## 1. Project Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac / Linux:**

```bash
source venv/bin/activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

---

## 2. Requirements

Create `requirements.txt` file:

```
yt-dlp
imageio-ffmpeg
```

---

## 3. Project Structure

```
video_downloader/
│
├── core/
│   ├── downloader.py
│   └── utils.py
│
├── videos/
├── urls.txt
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

---

## 4. How to Use

## URL List

Create a `urls.txt` file based on the example file:

```bash
copy urls.example.txt urls.txt
```

### Download Single Video

```bash
python main.py https://example.com/video
```

### Download Multiple Videos from TXT

```bash
python main.py urls.txt
```

Example `urls.txt`:

```
https://example.com/video1
https://example.com/video2
https://example.com/video3
```

---

## 5. Command Options

| Command                        | Description           |
| ------------------------------ | --------------------- |
| python main.py URL             | Download best quality |
| python main.py URL -q 720      | Download 720p         |
| python main.py URL -a          | Download audio only   |
| python main.py URL -s          | Simple mode (fast)    |
| python main.py urls.txt        | Batch download        |
| python main.py urls.txt -q 720 | Batch download 720p   |

---

## 6. Download Modes

| Mode   | Format                 | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| Best   | bestvideo+bestaudio    | Best quality (merge video + audio) |
| 720p   | bestvideo[height<=720] | Specific resolution                |
| Audio  | bestaudio              | Audio only                         |
| Simple | best                   | Fast download (single file)        |

---

## 7. Output Folder

All downloaded files will be saved in:

```
videos/
```

---

## 8. Running the Project

Each time you want to run the project:

**Windows:**

```bash
venv\Scripts\activate
python main.py urls.txt
```

**Mac / Linux:**

```bash
source venv/bin/activate
python main.py urls.txt
```

---

## 9. .gitignore

```
venv/
__pycache__/
videos/
*.mp4
```

---

## 10. Features

- Video download
- Audio download
- Batch download
- Resolution selection
- Simple mode
- CLI tool

---

## 11. Notes

If you download high quality video (video + audio separated), **FFmpeg is required**.

Check FFmpeg:

```bash
ffmpeg -version
```

---

## 12. Author

Built with Python and yt-dlp.
