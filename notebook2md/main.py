#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converts a Jupyter Notebook (.ipynb) file to Markdown format with cell delimiters and prints to stdout.
"""

import sys
import argparse
import os
import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
import pyperclip


class InjectCellDelimiters(Preprocessor):
    """
    Preprocessor that wraps each cell with start/end delimiter comments.
    """

    def preprocess_cell(self, cell, resources, index):
        cell_type = cell.cell_type
        start = f"<-- START:{index}:{cell_type} -->"
        end = f"<-- END:{index}:{cell_type} -->"

        if cell_type == "code" or cell_type == "markdown":
            lines = cell.source.strip().splitlines()
            cell.source = "\n".join([start] + lines + [end])
        else:
            # Leave other cell types unchanged
            pass

        return cell, resources


def convert_notebook_to_markdown(notebook_path):
    """
    Reads an .ipynb file, converts it to Markdown with cell delimiters, and returns the Markdown content.
    """
    try:
        if not os.path.isfile(notebook_path):
            print(f"Error: File not found at {notebook_path}", file=sys.stderr)
            return None

        exporter = MarkdownExporter()
        exporter.register_preprocessor(InjectCellDelimiters, enabled=True)

        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_node = nbformat.read(f, as_version=4)

        (markdown_output, _) = exporter.from_notebook_node(notebook_node)

        return markdown_output

    except nbformat.validator.NotebookValidationError as e:
        print(f"Error: Invalid notebook format in {notebook_path}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error converting notebook {notebook_path}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Jupyter Notebook (.ipynb) to Markdown with cell delimiters and print to stdout."
    )
    parser.add_argument("notebook_path", help="Path to the input .ipynb notebook file.")
    parser.add_argument("-c", "--clipboard", action="store_true", 
                        help="Copy the output to clipboard instead of printing to stdout")
    args = parser.parse_args()

    markdown_content = convert_notebook_to_markdown(args.notebook_path)

    if markdown_content is not None:
        if args.clipboard:
            try:
                pyperclip.copy(markdown_content)
                print(f"Markdown content from {args.notebook_path} copied to clipboard.", file=sys.stderr)
                sys.exit(0)
            except Exception as e:
                print(f"Error copying to clipboard: {e}", file=sys.stderr)
                print(markdown_content)
                sys.exit(1)
        else:
            print(markdown_content)
            sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
