# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

notebook2md is a command-line tool that converts Jupyter Notebooks (.ipynb) to Markdown format with special cell delimiter comments. The tool wraps each cell with `<-- START:index:type -->` and `<-- END:index:type -->` markers to preserve cell structure information in the markdown output.

## Architecture

### Dual Entry Points

The project has two main entry points that provide similar functionality with different feature sets:

1. **src/notebook2md/main.py** - Simple, focused implementation
   - Core conversion logic only
   - Outputs to stdout
   - No external dependencies beyond nbformat/nbconvert

2. **main.py** (root level) - Extended version with additional features
   - Includes clipboard support via `--clipboard/-c` flag using pyperclip
   - Environment configuration via ~/.repo2readme/.env
   - Colored console output for better UX
   - Note: The CONFIG_DIR path references "repo2readme" (likely from earlier project iteration)

The package entry point in pyproject.toml points to `notebook2md.main:main` (the simpler version in src/).

### Core Conversion Mechanism

Both implementations use the same approach:
- Custom `InjectCellDelimiters` preprocessor extends nbconvert's `Preprocessor` class
- Preprocessor wraps each code/markdown cell with delimiter comments during conversion
- Uses nbconvert's `MarkdownExporter` with the custom preprocessor registered

## Development Commands

```bash
# Install package locally for testing
pipx install . --force

# Run the tool
notebook2md path/to/notebook.ipynb
notebook2md --clipboard path/to/notebook.ipynb

# Test with sample notebook
notebook2md sample.ipynb > output.md
```

## Important Notes

- README.md must be kept up to date with any significant project changes
- The root main.py has an empty REQUIRED_VARS list - no environment variables are currently required despite the env setup code
- Cell delimiter format: `<-- START:index:cell_type -->` where cell_type is "code" or "markdown"
