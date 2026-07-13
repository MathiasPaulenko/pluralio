from __future__ import annotations

import re
from importlib.metadata import PackageNotFoundError
from pathlib import Path
from unittest.mock import patch

import pluralio


class TestReadVersion:
    def test_version_is_string(self) -> None:
        assert isinstance(pluralio.__version__, str)
        assert pluralio.__version__ != ""

    def test_version_matches_pyproject(self) -> None:
        pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(), re.M)
        assert match is not None
        assert pluralio.__version__ == match.group(1)

    def test_fallback_to_pyproject_when_not_installed(self) -> None:
        with patch("pluralio.version", side_effect=PackageNotFoundError):
            result = pluralio._read_version()
        pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(), re.M)
        assert match is not None
        assert result == match.group(1)

    def test_fallback_to_unknown_when_no_pyproject(self, tmp_path: Path) -> None:
        original_parent = Path(pluralio.__file__).resolve().parent

        fake_init = tmp_path / "pluralio_fake" / "__init__.py"
        fake_init.parent.mkdir()
        fake_init.write_text("")

        with (
            patch("pluralio.version", side_effect=PackageNotFoundError),
            patch.object(Path, "resolve", return_value=fake_init),
        ):
            result = pluralio._read_version()

        assert result == "0.0.0+unknown"
        _ = original_parent
