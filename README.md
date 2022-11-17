# Poetry Plugin Pyenv

This package aims to make working with [Poetry](https://python-poetry.org/) and [Pyenv](https://github.com/pyenv/pyenv) a seamless experience.

## Installation

The easist and *recommended* way to install is using Poetry's `self add` command.

```bash
poetry self add poetry-plugin-pyenv
```

If you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.

```bash
pipx inject poetry poetry-plugin-pyenv
```

Otherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.

```bash
pip install poetry-plugin-pyenv
```

## Usage

### Enabling

This plugin work in conjunction with the [`virtualenvs.prefer-active-python`](https://python-poetry.org/docs/configuration#virtualenvsprefer-active-python-experimental) option. Therefore the first step to using this plugin is enabling that option.

To enable the option locally you can use the following command.

```bash
poetry config virtualenvs.prefer-active-python true --local
```

To, instead, enable the option globally use the following command.

```bash
poetry config virtualenvs.prefer-active-python true
```

Once enabled this plugin should work transparently to enable seamless interoperability with [Poetry](https://python-poetry.org/) and [Pyenv](https://github.com/pyenv/pyenv). To learn more about what this plugin does behind the scenes see the [Behavior](#behavior) section.

## Behavior

[Poetry Plugin Pyenv](#poetry-plugin-pyenv) works by treating `python` constraint declared in the `tool.poetry.dependencies` of `pyproject.toml` as a source of truth for Pyenv's local python version. To do this it will exercise the following behavior.

### Pyenv already has a local version

If Pyenv already has a local version it will check if the local version matches the constraint specified in the `pyproject.toml`. If the constraint is not satisfied it will proceed to [selecting a new python version](#selecting-a-new-python-version). If the constraint is satisfied Poetry's virtualenv will be created using the local version thanks to [`virtualenvs.prefer-active-python`](https://python-poetry.org/docs/configuration#virtualenvsprefer-active-python-experimental).

### Pyenv has no local version

If Pyenv does not have a local version set it will proceed to [selecting a new python version](#selecting-a-new-python-version).

### Selecting a new python version

If a new python version needs to be selected the list of installable versions available to Pyenv will be checked against the constraint. From this list the latest possible version to satisfy the constraint will be selected. If this version is not installed it will be installed. It will then be set as Pyenv's local version and Poetry's virtualenv will be [re]created.
