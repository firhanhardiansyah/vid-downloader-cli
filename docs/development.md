# Development

## Set up the project

Clone the repository and synchronize its environment from `uv.lock`:

```bash
git clone https://github.com/firhanhardiansyah/vid-downloader-cli.git
cd vid-downloader-cli
uv sync
```

uv creates `.venv` automatically and installs the project in editable mode.
Activating the virtual environment is not required.

## Run the development version

```bash
uv run vdl
uv run vid-downloader
uv run python main.py download
```

`uv run` synchronizes the environment when necessary before starting the
command.

## Run tests

```bash
uv run python -m unittest discover -s tests -v
```

Or:

```bash
make test
```

## Make commands

| Command | Description |
|---|---|
| `make install` | Install/update the CLI as an isolated uv tool |
| `make reinstall` | Reinstall the tool from the current source |
| `make uninstall` | Remove the installed tool |
| `make sync` | Synchronize `.venv` from `uv.lock` |
| `make test` | Run all unit tests through uv |
| `make dev-install` | Install the global CLI in editable mode |

## Manage dependencies

Add a runtime dependency:

```bash
uv add package-name
```

Remove one:

```bash
uv remove package-name
```

Refresh locked dependency versions:

```bash
uv lock --upgrade
uv sync
```

Commit both `pyproject.toml` and `uv.lock` when dependencies change.

## Validate before committing

```bash
uv lock --check
uv run python -m unittest discover -s tests -v
git diff --check
```

## Project structure

```text
vid-downloader-cli/
├── docs/                  User and contributor documentation
├── tests/                 Unit tests
├── vid_downloader/        Application package
│   ├── cli.py             Argument parsing and command execution
│   ├── interactive.py     Interactive prompt workflow
│   ├── downloader.py      yt-dlp orchestration
│   ├── download_config.py Config parsing
│   ├── download_lock.py   Cross-process directory locking
│   └── output_naming.py   Duplicate filename handling
├── download.example.conf  Example batch configuration
├── main.py                Compatibility entry point
├── Makefile               Common uv shortcuts
├── pyproject.toml          Package metadata and dependencies
└── uv.lock                 Reproducible dependency lock
```

## Build the package

```bash
uv build
```

Build artifacts are written to `dist/`, which is ignored by Git.

## Test an installed build

```bash
uv tool install --force .
vdl --version
```

Use `uv run vdl` during normal development to avoid reinstalling after each
source change.
