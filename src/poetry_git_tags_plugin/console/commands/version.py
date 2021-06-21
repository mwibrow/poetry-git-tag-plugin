from cleo.helpers import option

from git import Repo
import os

from poetry.console.commands.version import VersionCommand as VersionCommandCore


class VersionCommand(VersionCommandCore):

    options = VersionCommandCore.options + [
        option("tag", "t", "Create git tags when bumping version"),
        option("prefix", "p", "Prefix string for git tag", flag=False, default="v"),
    ]

    def handle(self) -> None:
        super().handle()
        version = self.argument("version")
        if version and self.option("tag"):

            content = self.poetry.file.read()
            poetry_content = content["tool"]["poetry"]
            version_text = poetry_content["version"]

            prefix = self.option("prefix")
            tag = "{}{}".format(prefix, version_text)

            repo = Repo(os.path.dirname(self.poetry.file._path))

            repo.git.execute(["git", "commit", ".", "-m", tag])
            repo.git.execute(["git", "tag", "-a", "-m", tag, tag])

            self.line("Created tag <fg=green>{}</>".format(tag))
