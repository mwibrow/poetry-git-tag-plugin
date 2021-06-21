from typing import TYPE_CHECKING

from git import Repo
import os

from poetry.console.commands.version import VersionCommand as VersionCommandCore


class VersionCommand(VersionCommandCore):
    def handle(self) -> None:
        super().handle()

        content = self.poetry.file.read()
        poetry_content = content["tool"]["poetry"]
        poetry_git_tags = content["tool"].get("poetry-git-tags", {})
        version = self.argument("version")
        if version and poetry_git_tags.get("create"):

            prefix = poetry_git_tags.get("prefix", "v")

            version_text = poetry_content["version"]
            tagname = "{}{}".format(prefix, version_text)
            repo = Repo(os.path.dirname(self.poetry.file._path))

            repo.git.execute(["git", "commit", ".", "-m", tagname])
            repo.git.execute(["git", "tag", "-a", "-m", tagname, tagname])

            self.line("Created tag <fg=green>{}</>".format(tagname))
