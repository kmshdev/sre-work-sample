.PHONY: setup test smoke docs-check run clean

PYTHON ?= python3
VENV ?= .venv
PORT ?= 8080

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install -e ".[dev]"

test:
	$(VENV)/bin/python -m pytest

smoke:
	$(VENV)/bin/python -m sre_work_sample.cli smoke

docs-check:
	$(PYTHON) scripts/validate_candidate_docs.py

run:
	$(VENV)/bin/python -m sre_work_sample.server --port $(PORT)

clean:
	rm -rf $(VENV) .pytest_cache htmlcov .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
