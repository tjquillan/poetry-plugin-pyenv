from __future__ import annotations

from typing import TYPE_CHECKING

from cleo.events.console_events import COMMAND
from poetry.plugins.application_plugin import ApplicationPlugin

from . import pyenv


if TYPE_CHECKING:
    from cleo.events.console_command_event import ConsoleCommandEvent
    from cleo.events.event_dispatcher import EventDispatcher
    from poetry.console.application import Application
    from poetry.core.constraints.version import Version
    from poetry.poetry import Poetry


class PyenvPlugin(ApplicationPlugin):
    @staticmethod
    def factory() -> PyenvPlugin:
        return PyenvPlugin()

    def activate(self, application: Application) -> None:
        poetry = application.poetry

        prefer_active_python: bool = poetry.config.get(
            "virtualenvs.prefer-active-python"
        )

        if (
            prefer_active_python
            and (event_dispatcher := application.event_dispatcher) is not None
        ):
            event_dispatcher.add_listener(COMMAND, self.on_env_command, 1)

    def on_env_command(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:

        from poetry.console.commands.env_command import EnvCommand

        command = event.command

        if not isinstance(command, EnvCommand):
            return

        if command._env is not None:
            return

        from poetry.utils.env import EnvManager

        poetry = command.poetry
        io = event.io
        manager = EnvManager(poetry)

        if not (
            local_version := pyenv.get_local_version()
        ) or not poetry.package.python_constraint.allows(local_version):
            local_versions = self.get_allowed_versions(poetry)
            local_version = local_versions[-1]

            pyenv.ensure_installed(local_version)
            pyenv.set_local_version(local_version)
            env = manager.activate(local_version.text, io)
        else:
            pyenv.ensure_installed(local_version)
            env = manager.create_venv(io)

        command.set_env(env)
        if env.is_venv() and io.is_verbose():
            io.write_line(f"Using virtualenv: <comment>{env.path}</>")

    def get_allowed_versions(self, poetry: Poetry) -> list[Version]:
        versions = pyenv.get_remote_versions()
        return [
            v
            for v in versions
            if poetry.package.python_constraint.allows(v) and v.is_stable()
        ]
