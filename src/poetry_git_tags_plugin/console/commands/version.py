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
        version = self.argument("version")

        if version:
            version = self.increment_version(
                self.poetry.package.pretty_version, version
            )

            if self.option("short"):
                self.line("{}".format(version))
            else:
                self.line(
                    "Bumping version from <b>{}</> to <fg=green>{}</>".format(
                        self.poetry.package.pretty_version, version
                    )
                )

            content = self.poetry.file.read()
            poetry_content = content["tool"]["poetry"]
            poetry_content["version"] = version.text

            self.poetry.file.write(content)

            if self.option("tag"):

                prefix = self.option("prefix")
                tag = "{}{}".format(prefix, version.text)

                repo = Repo(os.path.dirname(self.poetry.file._path))

                assert not repo.bare
                repo.git.execute(["git", "commit", ".", "-m", tag])
                repo.git.execute(["git", "tag", "-a", "-m", tag, tag])

                self.line("Created tag <fg=green>{}</>".format(tag))
        else:
            if self.option("short"):
                self.line("{}".format(self.poetry.package.pretty_version))
            else:
                self.line(
                    "<comment>{}</> <info>{}</>".format(
                        self.poetry.package.name, self.poetry.package.pretty_version
                    )
                )
