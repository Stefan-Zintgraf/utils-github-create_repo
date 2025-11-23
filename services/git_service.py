"""Git operations helper for the GitHub Repository Creator."""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

from utils.logger import configure_logger


logger = configure_logger("git_service")


class GitService:
    """Encapsulates Git repository operations."""

    def __init__(self, repo_path: str | Path | None = None) -> None:
        self.repo_path = Path(repo_path or os.getcwd()).resolve()

    def _run_git_command(self, args: list[str], *, capture_output: bool = True) -> subprocess.CompletedProcess[str]:
        """Run a git command and return the completed process."""
        try:
            return subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
            )
        except Exception as exc:  # pragma: no cover
            logger.exception("Failed to run git command %s", args)
            return subprocess.CompletedProcess(args, 1, stdout="", stderr=str(exc))
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=capture_output,
            text=True,
        )

    def initialize_repo(self) -> bool:
        """Initialize a Git repository."""
        result = self._run_git_command(["init"])
        if result.returncode != 0:
            logger.error("git init failed for %s: %s", self.repo_path, result.stderr.strip())
            return False
        return True

    def create_gitkeep_files(self) -> int:
        """Create .gitkeep files in empty folders."""
        created = 0
        for root, _, files in os.walk(self.repo_path):
            current = Path(root)
            if ".git" in current.parts:
                continue

            if files:
                continue

            gitkeep_path = current / ".gitkeep"
            if gitkeep_path.exists():
                continue

            try:
                gitkeep_path.write_text("", encoding="utf-8")
                created += 1
            except OSError:
                logger.warning("Failed to write .gitkeep in %s, retrying", current)
                current.chmod(current.stat().st_mode | stat.S_IWUSR)
                try:
                    gitkeep_path.write_text("", encoding="utf-8")
                    created += 1
                except OSError:
                    continue

        return created

    def stage_all_files(self) -> tuple[int, int]:
        """Stage all files and report counts."""
        add_result = self._run_git_command(["add", "."])
        if add_result.returncode != 0:
            logger.error("git add failed: %s", add_result.stderr.strip())
            return 0, 0

        ls_result = self._run_git_command(["ls-files"])
        files = [line for line in ls_result.stdout.splitlines() if line]
        total_size = sum(
            (self.repo_path / file).stat().st_size
            for file in files
            if (self.repo_path / file).exists()
        )

        return len(files), total_size

    def commit(self, message: str) -> bool:
        """Create a commit."""
        result = self._run_git_command(["commit", "-m", message])
        if result.returncode != 0:
            logger.error("git commit failed: %s", result.stderr.strip())
            return False
        return True

    def add_remote(self, url: str) -> bool:
        """Add a remote origin, replacing an existing one if present."""
        self._run_git_command(["remote", "remove", "origin"])
        result = self._run_git_command(["remote", "add", "origin", url])
        if result.returncode != 0:
            logger.error("git remote add failed: %s", result.stderr.strip())
            return False
        return True

    def rename_branch(self, branch_name: str) -> bool:
        """Rename the current branch."""
        result = self._run_git_command(["branch", "-M", branch_name])
        if result.returncode != 0:
            logger.error("git branch rename failed: %s", result.stderr.strip())
            return False
        return True

    def push(self, branch: str, remote: str) -> bool:
        """Push to a remote repository."""
        result = self._run_git_command(["push", "-u", remote, branch])
        if result.returncode != 0:
            logger.error("git push failed: %s", result.stderr.strip())
            return False
        return True
