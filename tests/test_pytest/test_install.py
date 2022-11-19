from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.core.constraints.version import Version

from poetry_plugin_pyenv import pyenv


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_install(mocker: MockerFixture) -> None:
    test_version = Version.parse("3.11.0")

    subprocess_run = mocker.patch("subprocess.run")

    pyenv.install(test_version)

    subprocess_run.assert_called_once()
