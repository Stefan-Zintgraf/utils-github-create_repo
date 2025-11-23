"""Git operations helper for the GitHub Repository Creator."""

from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path


class GitService:
    """Encapsulates Git repository operations."""

    def __init__(self, repo_path: str | Path | None = None) -> None:
        self.repo_path = Path(repo_path or os.getcwd()).resolve()

    def _run_git_command(self, args: list[str], *, capture_output: bool = True) -> subprocess.CompletedProcess[str]:
        """Run a git command and return the completed process."""
        return subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=capture_output,
            text=True,
        )

    def initialize_repo(self) -> bool:
        """Initialize a Git repository."""
        result = self._run_git_command(["init"])
        return result.returncode == 0

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
        return result.returncode == 0

    def add_remote(self, url: str) -> bool:
        """Add a remote origin, replacing an existing one if present."""
        self._run_git_command(["remote", "remove", "origin"])
        result = self._run_git_command(["remote", "add", "origin", url])
        return result.returncode == 0

    def rename_branch(self, branch_name: str) -> bool:
        """Rename the current branch."""
        result = self._run_git_command(["branch", "-M", branch_name])
        return result.returncode == 0

    def push(self, branch: str, remote: str) -> bool:
        """Push to a remote repository."""
        result = self._run_git_command(["push", "-u", remote, branch])
        return result.returncode == 0
