#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor
from pathlib import Path
from dotenv import load_dotenv
import pyperclip
import shutil

# Constants
CONFIG_DIR = Path.home() / ".repo2readme"
ENV_PATH = CONFIG_DIR / ".env"
REQUIRED_VARS = []
RED, GREEN, RESET = '\033[31m', '\033[32m', '\033[0m'


def log(color, msg): print(f"{color}{msg}{RESET}")
def fatal(msg): log(RED, msg); sys.exit(1)


class InjectCellDelimiters(Preprocessor):
    """Add START/END comments around each code or markdown cell."""
    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type in ("code", "markdown"):
            marker = f"<-- {{}}:{index}:{cell.cell_type} -->"
            lines = cell.source.strip().splitlines()
            cell.source = "\n".join([marker.format("START")] + lines + [marker.format("END")])
        return cell, resources


def setup_env():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not ENV_PATH.exists():
        try:
            shutil.copy(Path(__file__).parent / "configs" / ".env.example", ENV_PATH)
            log(GREEN, f"✅ Created default env: {ENV_PATH}")
            print(f"⚠️  Edit with: nano {ENV_PATH}")
        except Exception as e:
            fatal(f"❌ Couldn't create .env: {e}")
        sys.exit(1)

    load_dotenv(dotenv_path=ENV_PATH, override=True)
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        fatal(f"Missing env vars: {', '.join(missing)}")


def convert_notebook(path):
    if not Path(path).is_file():
        fatal(f"❌ File not found: {path}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        exporter = MarkdownExporter()
        exporter.register_preprocessor(InjectCellDelimiters, enabled=True)
        markdown, _ = exporter.from_notebook_node(notebook)
        return markdown
    except Exception as e:
        fatal(f"❌ Conversion failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert .ipynb → Markdown with cell markers.")
    parser.add_argument("notebook_path", help="Path to the .ipynb file.")
    parser.add_argument("-c", "--clipboard", action="store_true", help="Copy output to clipboard.")
    args = parser.parse_args()

    setup_env()
    md = convert_notebook(args.notebook_path)

    if args.clipboard:
        try:
            pyperclip.copy(md)
            log(GREEN, f"📋 Markdown copied to clipboard from: {args.notebook_path}")
        except Exception as e:
            log(RED, f"⚠️  Clipboard failed: {e}")
            print(md)
            sys.exit(1)
    else:
        print(md)


if __name__ == "__main__":
    main()
