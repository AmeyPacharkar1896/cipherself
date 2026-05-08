# cipher Tests

This directory contains integration tests for the `cipher` CLI tool.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed and synced (`uv sync`).

## Running Tests

You can run the tests using Python's built-in `unittest` module or `pytest` if installed.

### Using unittest (Recommended)

```bash
uv run python -m unittest discover tests
```

### Using pytest (If installed)

```bash
uv run pytest tests
```

## Test Coverage

- **CLI Validation**: Verifies that required flags are handled and error messages are printed for invalid inputs.
- **Output Organization**: Asserts that PDF reports are saved into the correct subdirectories (`outputs/demo/`, `outputs/github/`, etc.) based on the source flags used.
- **Integration**: Runs real (but limited) data collection to ensure the full end-to-end flow is stable.

## Manual API Debugging

If you encounter rate limits or connection issues during standard CLI use, there are standalone scratch scripts available in the `manual_scripts/` directory to manually verify the individual endpoints:

- `manual_scripts/test_apis.py`: Prints raw JSON responses for the GitHub Profile and Reddit Profile APIs.
- `manual_scripts/test_search_api.py`: Directly tests the DuckDuckGo Lite search endpoint with `requests` and `BeautifulSoup` to ensure parsing is working.

You can run them via:
```bash
uv run python tests/manual_scripts/test_apis.py
uv run python tests/manual_scripts/test_search_api.py
```

> [!NOTE]
> Tests that involve `--github`, `--reddit`, or `--name` (without `--demo`) will perform actual network requests and may take longer to complete.
