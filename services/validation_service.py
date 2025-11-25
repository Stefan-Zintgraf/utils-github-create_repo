"""Input validation helpers for the GitHub Repository Creator."""

from __future__ import annotations

import os
import re
from pathlib import Path

VALID_REPO_NAME = re.compile(r"^(?=.{1,100}$)[A-Za-z0-9._-]+$")
VALID_TOKEN_PREFIXES = ("ghp_", "gho_", "ghu_", "ghr_", "ghs_", "ghk_", "github_pat_")


class ValidationService:
    """Utility class for GitHub Repository Creator input validation."""

    @staticmethod
    def validate_folder_path(path: str) -> tuple[bool, str]:
        """Verify that a folder path is valid and ready for repository creation."""
        if not path:
            return False, "Folder path must not be empty."

        folder = Path(path)
        if not folder.exists():
            return False, "Folder path does not exist."
        if not folder.is_dir():
            return False, "Folder path is not a directory."
        if not os.access(folder, os.R_OK):
            return False, "Folder path is not readable."
        if (folder / ".git").exists():
            return False, "Folder already contains a Git repository."

        return True, "Folder path is valid."

    @staticmethod
    def validate_repository_name(name: str) -> tuple[bool, str]:
        """Validate repository name format against GitHub requirements."""
        if not name or not name.strip():
            return False, "Repository name must not be empty."
        if VALID_REPO_NAME.match(name) is None:
            return False, (
                "Repository names can only include letters, numbers, hyphens, underscores, or periods (1-100 characters)."
            )
        if name.endswith("."):
            return False, "Repository name must not end with a period."

        return True, "Repository name is valid."

    @staticmethod
    def validate_token(token: str) -> tuple[bool, str]:
        """Validate GitHub Personal Access Token format."""
        if not token or not token.strip():
            return False, "Token must not be empty."

        token = token.strip()
        if len(token) < 40:
            return False, "Token appears too short."
        if not token.startswith(VALID_TOKEN_PREFIXES):
            return False, "Token must start with a valid GitHub token prefix (e.g., ghp_ for classic tokens or github_pat_ for fine-grained tokens)."

        return True, "Token format looks valid."
