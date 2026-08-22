UV ?= uv
PACKAGE_NAME := vid-downloader-cli

.PHONY: install reinstall uninstall test dev-install check-uv sync

check-uv:
	@$(UV) --version

install: check-uv
	$(UV) tool install --force .
	$(UV) tool update-shell

reinstall: check-uv
	$(UV) tool install --force .

uninstall: check-uv
	$(UV) tool uninstall $(PACKAGE_NAME)

sync: check-uv
	$(UV) sync

test: check-uv
	$(UV) run python -m unittest discover -s tests -v

dev-install: check-uv
	$(UV) tool install --force --editable .
	$(UV) tool update-shell
