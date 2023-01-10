from __future__ import annotations

from typing import TYPE_CHECKING

from cleo.events.console_events import COMMAND
from poetry.plugins.application_plugin import ApplicationPlugin

from . import pyenv


if TYPE_CHECKING:
    from cleo.events.event import Event
    from cleo.events.event_dispatcher import EventDispatcher
    from poetry.console.application import Application
    from poetry.core.constraints.version import Version
    from poetry.poetry import Poetry


class PyenvPlugin(ApplicationPlugin):
    @staticmethod
    def factory() -> PyenvPlugin:
        return PyenvPlugin()

    def activate(self, application: Application) -> None:
        if (event_dispatcher := application.event_dispatcher) is not None:
            # Insert with priority higher than Application.configure_env hook
            event_dispatcher.add_listener(COMMAND, self.configure_pyenv, 1)

    def configure_pyenv(
        self, event: Event, event_name: str, dispatcher: EventDispatcher
    ) -> None:

        from cleo.events.console_command_event import ConsoleCommandEvent
        from poetry.console.commands.env_command import EnvCommand
        from poetry.console.commands.self.self_command import SelfCommand

        if not isinstance(event, ConsoleCommandEvent):
            return

        command = event.command

        if not isinstance(command, EnvCommand) or isinstance(command, SelfCommand):
            return

        if command._env is not None:
            return

        poetry = command.poetry
        prefer_active_python: bool = poetry.config.get(
            "virtualenvs.prefer-active-python"
        )
        if not prefer_active_python:
            return

        from poetry.utils.env import EnvManager

        poetry = command.poetry
        io = event.io
        manager = EnvManager(poetry, io=io)

        create = False
        if not (
            local_version := pyenv.get_local_version()
        ) or not poetry.package.python_constraint.allows(local_version):
            local_versions = self.get_allowed_versions(poetry)
            local_version = local_versions[-1]
            create = True

        pyenv.ensure_installed(local_version)
        if create:
            pyenv.set_local_version(local_version)
        env = manager.create_venv(force=create)

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
