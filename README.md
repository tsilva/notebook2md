# notebook2md

<p align="center">
  <img src="logo.png" alt="notebook2md" width="400"/>
</p>

A lightweight utility to convert Jupyter Notebooks (.ipynb) to Markdown format with cell delimiters.

## Description

notebook2md is a simple command-line tool that converts Jupyter Notebook files to Markdown format while preserving cell structure information using delimiter comments. This makes it easier to track and identify different cells when working with the exported Markdown content.

## Features

- Converts Jupyter Notebooks to Markdown
- Adds distinct delimiters for code and markdown cells
- Preserves cell numbering and type information
- Simple command-line interface

## Installation

### Using pipx (recommended)

For a clean, isolated installation that doesn't affect your global Python environment:

```bash
# Install the latest published version
pipx install notebook2md

# Or install from your local clone
pipx install .
```

### Using pip

```bash
pip install notebook2md
```

### Development installation

Clone the repository and install using Hatch:

```bash
git clone https://github.com/tsilva/notebook2md.git
cd notebook2md
pipx install .
```

## Usage

After installation, you can use notebook2md directly from the command line:

```bash
notebook2md path/to/your/notebook.ipynb > output.md
```

The tool prints the converted Markdown to stdout, allowing you to redirect it to a file or pipe it to another command.

### Output Format

Each cell in the notebook is wrapped with delimiter comments indicating:
- Cell index
- Cell type (code or markdown)

Example:
```
<-- START:0:markdown -->
# This is a markdown cell
<-- END:0:markdown -->

<-- START:1:code -->
print("This is a code cell")
<-- END:1:code -->
```

## License

MIT
