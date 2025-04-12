# Publishing Guide for fetch-my-weather

This guide walks you through the process of publishing your `fetch-my-weather` package to PyPI using modern Python tooling.

## Prerequisites

Make sure you have the following installed:

```bash
# Install uv for environment and package management
pip install uv

# Create and activate virtual environment with uv
uv venv
source .venv/bin/activate  # On Unix/MacOS
# .venv\Scripts\activate  # On Windows

# Install development dependencies
uv pip install -e ".[dev]"
```

You'll also need accounts on:
- [PyPI](https://pypi.org/account/register/) (for final publishing)
- [TestPyPI](https://test.pypi.org/account/register/) (for testing)

## Step 1: Update Your Package Information

Edit the following files with your personal information:

1. `pyproject.toml`: Update the author name, email, and GitHub username
2. `LICENSE`: Add your name and the current year
3. `README.md`: Make any final adjustments to the documentation

## Step 2: Validate Your Code

Before publishing, verify that your code passes all quality checks:

```bash
# Type checking with mypy
mypy src/fetch_my_weather

# Linting with ruff
ruff check src/fetch_my_weather

# Formatting with ruff
ruff format src/fetch_my_weather

# Run tests with pytest
pytest
```

## Step 3: Build Your Package

From the root directory of your project, run:

```bash
python -m build
```

This will create two files in the `dist/` directory:
- A source distribution (`.tar.gz`)
- A wheel (`.whl`)

## Step 4: Test Your Package on TestPyPI

Upload to TestPyPI first to make sure everything works:

```bash
# Using twine 6.0.1 as specified
twine upload --repository testpypi dist/*
```

You'll be prompted for your TestPyPI username and password.

## Step 5: Verify Your TestPyPI Upload

Create a new virtual environment and try installing your package from TestPyPI:

```bash
# Create and activate a clean virtual environment with uv
uv venv test_env
source test_env/bin/activate  # On Unix/MacOS
# test_env\Scripts\activate  # On Windows

# Install your package from TestPyPI
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fetch-my-weather

# Test that it works
python -c "import fetch_my_weather; print(fetch_my_weather.__version__)"
```

## Step 6: Publish to Real PyPI

If everything looks good on TestPyPI, upload to the real PyPI:

```bash
twine upload dist/*
```

## Step 7: Verify Your PyPI Upload

Create another fresh virtual environment and install your package from the real PyPI:

```bash
# Create and activate a clean virtual environment with uv
uv venv verify_env
source verify_env/bin/activate  # On Unix/MacOS
# verify_env\Scripts\activate  # On Windows

# Install your package from PyPI
uv pip install fetch-my-weather

# Test that it works
python -c "import fetch_my_weather; print(fetch_my_weather.__version__)"
```

## Congratulations!

Your `fetch-my-weather` package is now published and available for anyone to install using `pip install fetch-my-weather`!

## Updating Your Package Later

When you want to release a new version:

1. Update the version number in `fetch_my_weather/__init__.py`
2. Make your code changes
3. Run quality checks (mypy, ruff, pytest)
4. Rebuild using `python -m build`
5. Upload the new version with `twine upload dist/*`

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [Packaging Python Projects Tutorial](https://packaging.python.org/tutorials/packaging-projects/)
- [TestPyPI Guide](https://packaging.python.org/guides/using-testpypi/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [ruff Documentation](https://github.com/astral-sh/ruff)
- [mypy Documentation](https://mypy.readthedocs.io/)