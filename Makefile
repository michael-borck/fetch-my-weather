.PHONY: clean lint format type-check test build publish-test publish help

help:
	@echo "Available commands:"
	@echo "  make clean       - Remove build artifacts and cache directories"
	@echo "  make lint        - Run linting with ruff"
	@echo "  make format      - Run code formatting with ruff"
	@echo "  make type-check  - Run type checking with mypy"
	@echo "  make test        - Run tests with pytest"
	@echo "  make build       - Build package distribution files"
	@echo "  make publish-test- Publish to TestPyPI"
	@echo "  make publish     - Publish to PyPI"

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

lint:
	ruff check src/simple_weather tests examples

format:
	ruff format src/simple_weather tests examples

type-check:
	mypy src/simple_weather

test:
	pytest -v

build: clean
	python -m build

publish-test: build
	twine upload --repository testpypi dist/*

publish: build
	twine upload dist/*