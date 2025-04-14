.PHONY: clean lint format type-check test build publish-test publish docs-serve docs-build docs-deploy help

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
	@echo "  make docs-serve  - Serve MkDocs documentation locally"
	@echo "  make docs-build  - Build MkDocs documentation site"
	@echo "  make docs-deploy - Deploy documentation to GitHub Pages"

clean:
	rm -rf build dist *.egg-info site
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

lint:
	ruff check src/fetch_my_weather tests examples

format:
	ruff format src/fetch_my_weather tests examples

type-check:
	mypy src/fetch_my_weather

test:
	pytest -v

build: clean
	python -m build

publish-test: build
	twine upload --repository testpypi dist/*

publish: build
	twine upload dist/*

docs-serve:
	mkdocs serve

docs-build:
	mkdocs build

docs-deploy:
	mkdocs gh-deploy --force