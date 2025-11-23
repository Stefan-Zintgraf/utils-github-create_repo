"""GitHub API operations for the GitHub Repository Creator."""

from __future__ import annotations

from typing import Optional

from github import Github
from github.GithubException import GithubException, UnknownObjectException

from utils.logger import configure_logger


logger = configure_logger("github_service")


class GitHubService:
    """Wraps PyGithub interactions."""

    def __init__(self, token: str):
        self.token = token.strip()
        self.client: Optional[Github] = Github(self.token) if self.token else None

    def validate_token(self, token: str) -> bool:
        """Validate the provided GitHub token by fetching the current user."""
        if not token or not self.client:
            logger.warning("Token validation skipped; missing token or client.")
            return False

        try:
            user = self.client.get_user()
            return bool(user.login)
        except GithubException as exc:
            logger.error("Token validation failed: %s", exc)
            return False

    def create_repository(self, name: str, private: bool, description: str) -> str:
        """Create a repository and return its clone URL."""
        if not self.client:
            logger.error("Cannot create repository; missing GitHub client.")
            raise GithubException(0, "Missing token", {})

        try:
            user = self.client.get_user()
            repository = user.create_repo(
                name=name,
                private=private,
                description=description,
                auto_init=False,
            )
            return repository.clone_url
        except GithubException as exc:
            logger.error("Repository creation failed: %s", exc)
            raise

    def check_repository_exists(self, name: str) -> bool:
        """Return True if the repository exists for the authenticated user."""
        if not self.client:
            logger.warning("Repository existence check skipped; missing client.")
            return False

        try:
            user = self.client.get_user()
            user.get_repo(name)
            return True
        except UnknownObjectException:
            return False
        except GithubException as exc:
            logger.error("Repository existence check failed: %s", exc)
            return False
