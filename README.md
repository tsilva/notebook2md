<div align="center">
  <img src="logo.png" alt="notebook2md" width="512"/>

  [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.12+-3776ab.svg)](https://python.org)

  **📓 Convert Jupyter Notebooks to Markdown with cell structure preserved ✨**

</div>

## Overview

notebook2md transforms Jupyter Notebook files (.ipynb) into Markdown while preserving cell boundaries with special delimiter comments. Each cell is wrapped with `<-- START:index:type -->` and `<-- END:index:type -->` markers, making it easy to identify and track cell structure in the output.

## Features

- Preserves cell structure with delimiter markers
- Supports both code and markdown cells
- Copy output directly to clipboard with `-c` flag
- Lightweight with minimal dependencies

## Quick Start

```bash
pipx install notebook2md
```

```bash
# Output to stdout
notebook2md notebook.ipynb > output.md

# Copy to clipboard
notebook2md -c notebook.ipynb
```

## Output Format

Each cell in the notebook is wrapped with delimiter comments:

```markdown
<-- START:0:markdown -->
# This is a markdown cell
<-- END:0:markdown -->

<-- START:1:code -->
print("This is a code cell")
<-- END:1:code -->
```

## Installation

### From Source

```bash
git clone https://github.com/tsilva/notebook2md.git
cd notebook2md
pipx install . --force
```

### Requirements

- Python 3.12+
- nbformat
- nbconvert
- pyperclip (for clipboard support)

## Usage

```bash
# Basic conversion to stdout
notebook2md path/to/notebook.ipynb

# Redirect to file
notebook2md path/to/notebook.ipynb > output.md

# Copy to clipboard
notebook2md --clipboard path/to/notebook.ipynb
notebook2md -c path/to/notebook.ipynb
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
