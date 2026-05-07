# cipherself Tests

This directory contains integration tests for the `cipherself` CLI tool.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed and synced (`uv sync`).
- [poppler](https://poppler.freedesktop.org/) installed (for PDF-to-PNG demo conversion).

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

> [!NOTE]
> Tests that involve `--github`, `--reddit`, or `--name` (without `--demo`) will perform actual network requests and may take longer to complete.
