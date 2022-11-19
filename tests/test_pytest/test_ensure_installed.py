from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.core.constraints.version import Version

from poetry_plugin_pyenv import pyenv


if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def test_is_installed(mocker: MockerFixture) -> None:
    test_version = Version.parse("3.12-dev")

    pyenv_install = mocker.patch("poetry_plugin_pyenv.pyenv.install")
    pyenv_is_installed = mocker.patch("poetry_plugin_pyenv.pyenv.is_installed")
    pyenv_is_installed.return_value = True

    pyenv.ensure_installed(test_version)

    pyenv_install.assert_not_called()


def test_is_not_installed(mocker: MockerFixture) -> None:
    test_version = Version.parse("3.12-dev")

    pyenv_install = mocker.patch("poetry_plugin_pyenv.pyenv.install")
    pyenv_is_installed = mocker.patch("poetry_plugin_pyenv.pyenv.is_installed")
    pyenv_is_installed.return_value = False

    pyenv.ensure_installed(test_version)

    pyenv_install.assert_called_once()
