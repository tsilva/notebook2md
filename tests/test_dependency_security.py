from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

import bleach
import nbformat
from packaging.version import Version

from notebook2md.main import convert_notebook


def test_vulnerable_dependency_families_resolve_to_safe_versions():
    minimum_versions = {
        "bleach": "6.4.0",
        "mistune": "3.3.0",
        "soupsieve": "2.8.4",
        "tornado": "6.5.7",
    }

    for package, minimum in minimum_versions.items():
        assert Version(version(package)) >= Version(minimum), package


def test_converter_never_enters_bleach_email_linkification(tmp_path: Path):
    payload = ("a." * 15_000) + "a"
    notebook_path = tmp_path / "hostile-email-pattern.ipynb"
    notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(payload)])
    nbformat.write(notebook, notebook_path)

    with (
        patch("bleach.linkify", side_effect=AssertionError("Bleach linkify was reached")),
        patch.object(
            bleach.linkifier.Linker,
            "linkify",
            side_effect=AssertionError("Bleach Linker was reached"),
        ),
    ):
        markdown = convert_notebook(str(notebook_path))

    assert payload in markdown


def test_uv_lock_uses_only_pypi_and_the_local_project():
    lockfile = Path("uv.lock").read_text(encoding="utf8")

    assert 'source = { editable = "." }' in lockfile
    assert "source = { git = " not in lockfile
    assert "source = { url = " not in lockfile
    assert "source = { path = " not in lockfile
    assert "source = { directory = " not in lockfile
    for line in lockfile.splitlines():
        if line.startswith("source = { registry = "):
            assert line == 'source = { registry = "https://pypi.org/simple" }'


def test_uv_supply_chain_policy_remains_enabled():
    pyproject = Path("pyproject.toml").read_text(encoding="utf8")

    assert 'exclude-newer = "7 days"' in pyproject
    assert '"bleach!=6.3.0"' in pyproject
    assert '"mistune>=3.3.0"' in pyproject
    assert '"soupsieve>=2.8.4"' in pyproject
