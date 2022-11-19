from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.core.constraints.version import Version

from poetry_plugin_pyenv import pyenv


if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


def test_get_remote_versions(datadir: Path, mocker: MockerFixture) -> None:
    expected_version = Version.parse("3.12-dev")

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.stdout = (datadir / "pyenv_install_l.txt").read_bytes()
    subprocess_run.return_value.returncode = 0

    output = pyenv.get_remote_versions()[-1]

    subprocess_run.assert_called_once()
    assert output == expected_version
    assert output.text == expected_version.text
