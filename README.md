# 📓 notebook2md

🔄 Convert Jupyter Notebooks to Markdown with cell delimiters and structure preservation

## 📖 Overview

notebook2md is a lightweight command-line tool that converts Jupyter Notebook (.ipynb) files to Markdown format while preserving cell structure information. It adds special delimiter comments to mark the beginning and end of each cell, making it easier to track and identify different cells in the exported Markdown content.

The tool is perfect for documentation workflows, version control of notebook content, or any scenario where you need a plain text representation of your notebooks with cell structure intact.

## 🚀 Installation

```bash
pipx install . --force
```

## 🛠️ Usage

After installation, you can use notebook2md directly from the command line:

```bash
# Output to stdout (can be redirected to a file)
notebook2md path/to/your/notebook.ipynb > output.md

# Copy directly to clipboard
notebook2md --clipboard path/to/your/notebook.ipynb
# or shorter form
notebook2md -c path/to/your/notebook.ipynb
```

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

## 📄 License

This project is licensed under the [MIT License](LICENSE).