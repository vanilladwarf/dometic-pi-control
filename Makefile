PROJECT := dometic-pi-control
PYTHON  := python3

.PHONY: help install dev test clean

help:
	@echo "$(PROJECT) targets:"
	@echo "  make install - install runtime deps"
	@echo "  make dev     - install dev deps"
	@echo "  make test    - run all tests"
	@echo "  make clean   - remove build artifacts"

install:
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install --upgrade pip wheel
	$(PYTHON) -m pip install -e .

dev:
	$(PYTHON) -m venv .venv
	$(PYTHON) -m pip install --upgrade pip wheel
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest tests/ --no-cov

clean:
	rm -rf build/ dist/ *.egg-info src/*.egg-info
	rm -rf .pytest_cache/ htmlcov/ .coverage
