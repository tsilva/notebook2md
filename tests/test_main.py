from pathlib import Path

import nbformat
import pytest

from notebook2md.main import convert_notebook


def write_notebook(path: Path) -> None:
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_markdown_cell("# Heading"),
            nbformat.v4.new_code_cell("print('hello')"),
        ]
    )
    nbformat.write(notebook, path)


def test_convert_notebook_to_markdown_adds_cell_markers(tmp_path):
    notebook_path = tmp_path / "sample.ipynb"
    write_notebook(notebook_path)

    markdown = convert_notebook(str(notebook_path))

    assert markdown is not None
    assert "<-- START:0:markdown -->" in markdown
    assert "<-- END:0:markdown -->" in markdown
    assert "<-- START:1:code -->" in markdown
    assert "<-- END:1:code -->" in markdown


def test_convert_notebook_to_markdown_returns_none_for_missing_file(tmp_path):
    with pytest.raises(SystemExit) as excinfo:
        convert_notebook(str(tmp_path / "missing.ipynb"))

    assert excinfo.value.code == 1
