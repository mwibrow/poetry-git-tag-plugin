# Poetry git tags plugin

This package is a plugin that allows creation of git tags when
bumping versons with `poetry version`.

**This repo is highly experimental**

## Installation

The easiest way to install the `poetry-git-tags-plugin` plugin is via `pip`:


```bash
pip install git+ssh://git@github.com/cloudfind/poetry-git-tags-plugin.git#main
```


## Usage

The plugin requires enties in the `pyproject.toml` file, for example:

```toml
[tool.poetry-git-tags]
create = true
prefix = "v"
```

The `create` setting is required for tags to be created.
By default the prefix is `v`.

```bash
poetry export -f requirements.txt --output requirements.txt
```

## Notes

This plug-in was more-or-less hacked together from 
the (poetry-export-plugin)[https://github.com/python-poetry/poetry-export-plugin].