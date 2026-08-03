PIPX ?= pipx
PYTHON ?= python3
PACKAGE_NAME := vid-downloader-cli

.PHONY: install reinstall uninstall test dev-install check-pipx

check-pipx:
	@command -v $(PIPX) >/dev/null 2>&1 || { \
		echo "pipx is not installed or not available in PATH."; \
		echo "macOS: brew install pipx"; \
		echo "Linux: $(PYTHON) -m pip install --user pipx"; \
		exit 1; \
	}

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
