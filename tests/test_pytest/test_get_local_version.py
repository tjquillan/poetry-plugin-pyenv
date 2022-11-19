from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.core.constraints.version import Version

from poetry_plugin_pyenv import pyenv


if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


def test_has_local_version(datadir: Path, mocker: MockerFixture) -> None:
    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.stdout = (
        datadir / "pyenv_local_valid.txt"
    ).read_bytes()
    subprocess_run.return_value.returncode = 0

    expected_version = Version.parse("3.11.0")
    actual_version = pyenv.get_local_version()

    subprocess_run.assert_called_once()
    assert actual_version == expected_version


def test_has_no_local_version(mocker: MockerFixture) -> None:
    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.returncode = 1

    expected_version = None
    actual_version = pyenv.get_local_version()

    subprocess_run.assert_called_once()
    assert actual_version == expected_version
