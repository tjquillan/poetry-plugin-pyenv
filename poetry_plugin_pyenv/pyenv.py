from __future__ import annotations

import re
import subprocess

from typing import TYPE_CHECKING

from poetry.core.constraints.version import Version


if TYPE_CHECKING:
    from re import Match
    from re import Pattern
    from subprocess import CompletedProcess
    from typing import Iterator


# See: https://regex101.com/r/Bz2g17/1
PYTHON_VERSION_REGEX: Pattern[str] = re.compile(
    r"^\s*(\d+\S*)\s*$", re.IGNORECASE | re.MULTILINE
)


def is_installed(version: Version) -> bool:
    result: CompletedProcess[bytes] = subprocess.run(
        ["pyenv", "versions", "--bare"], capture_output=True
    )
    return (
        result.returncode == 0
        and re.search(version.text, result.stdout.decode("utf-8"), flags=re.MULTILINE)
        is not None
    )


def install(version: Version) -> None:
    subprocess.run(["pyenv", "install", version.text], check=True)


def ensure_installed(version: Version) -> None:
    if not is_installed(version):
        install(version)


def get_local_version() -> Version | None:
    result: CompletedProcess[bytes] = subprocess.run(
        ["pyenv", "local"], capture_output=True
    )
    if result.returncode != 0:
        return None
    return Version.parse(result.stdout.decode("utf-8"))


def set_local_version(version: Version) -> None:
    subprocess.run(["pyenv", "local", version.text])


def get_remote_versions() -> list[Version]:
    result: CompletedProcess[bytes] = subprocess.run(
        ["pyenv", "install", "--list"], check=True, capture_output=True
    )
    output: str = result.stdout.decode("utf-8")
    matched_versions: Iterator[Match[str]] = re.finditer(PYTHON_VERSION_REGEX, output)
    return [Version.parse(v.group(1)) for v in matched_versions]
