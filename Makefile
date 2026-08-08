PIPX ?= pipx
PACKAGE_NAME := vid-downloader-cli

ifeq ($(OS),Windows_NT)
PYTHON ?= py
else
PYTHON ?= python3
endif

.PHONY: install reinstall uninstall test dev-install check-pipx

check-pipx:
	@$(PYTHON) -c "import shutil, sys; found = shutil.which('$(PIPX)'); print('pipx is not installed or not available in PATH.\nmacOS: brew install pipx\nLinux: python3 -m pip install --user pipx\nWindows: py -m pip install --user pipx') if not found else None; sys.exit(0 if found else 1)"

install: check-pipx
	$(PIPX) ensurepath
	$(PIPX) install --force .

reinstall: check-pipx
	$(PIPX) reinstall $(PACKAGE_NAME)

uninstall: check-pipx
	$(PIPX) uninstall $(PACKAGE_NAME)

test:
	$(PYTHON) -m unittest discover -s tests -v

dev-install: check-pipx
	$(PIPX) ensurepath
	$(PIPX) install --force --editable .
