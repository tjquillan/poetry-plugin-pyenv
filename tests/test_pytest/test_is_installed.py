from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.core.constraints.version import Version

from poetry_plugin_pyenv import pyenv


if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


def test_valid_version(datadir: Path, mocker: MockerFixture) -> None:
    test_version = Version.parse("3.11.0")

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.stdout = (
        datadir / "pyenv_versions_bare.txt"
    ).read_bytes()
    subprocess_run.return_value.returncode = 0

    assert pyenv.is_installed(test_version)
    subprocess_run.assert_called_once()


def test_invalid_version(datadir: Path, mocker: MockerFixture) -> None:
    test_version = Version.parse("3.12.0")

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.stdout = (
        datadir / "pyenv_versions_bare.txt"
    ).read_bytes()
    subprocess_run.return_value.returncode = 0

    assert not pyenv.is_installed(test_version)
    subprocess_run.assert_called_once()


def test_invalid_returncode(datadir: Path, mocker: MockerFixture) -> None:
    test_version = Version.parse("3.11.0")

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.stdout = (
        datadir / "pyenv_versions_bare.txt"
    ).read_bytes()
    subprocess_run.return_value.returncode = 1

    assert not pyenv.is_installed(test_version)
    subprocess_run.assert_called_once()
