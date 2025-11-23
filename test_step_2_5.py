# test_step_2_5.py
import os
import sys
from unittest import mock

from github.GithubException import GithubException, UnknownObjectException

from services.github_service import GitHubService


def test_github_service_methods() -> bool:
    errors = []

    with mock.patch("services.github_service.Github") as mock_github:
        mock_client = mock_github.return_value
        mock_user = mock.Mock()
        mock_user.login = "automation-user"
        repo_mock = mock.Mock()
        repo_mock.clone_url = "https://example.com/repo.git"
        mock_user.create_repo.return_value = repo_mock
        mock_user.get_repo.side_effect = [
            repo_mock,
            UnknownObjectException(404, "Not Found", {}),
        ]
        mock_client.get_user.return_value = mock_user

        service = GitHubService("ghp_exampletoken1234567890")

        if not service.validate_token("ghp_exampletoken1234567890"):
            errors.append("validate_token should return True for a mocked valid context.")

        created_url = service.create_repository("my-repo", private=True, description="Test repo")
        if created_url != repo_mock.clone_url:
            errors.append("Repository clone URL returned by create_repository is incorrect.")

        if not service.check_repository_exists("my-repo"):
            errors.append("Existing repository reported as missing.")

        if service.check_repository_exists("does-not-exist"):
            errors.append("Missing repository reported as existing.")

        mock_client.get_user.side_effect = GithubException(401, "Unauthorized", {})
        if service.validate_token("ghp_exampletoken1234567890"):
            errors.append("validate_token should return False when GitHub raises GitHubException.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_5_success.log", "w", encoding="utf-8") as f:
        f.write("Step 2.5: GitHub service verified with mocks.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_5_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 2.5 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(2, "2.5", True)
        print("Checklist updated for Step 2.5")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_github_service_methods()
    if success:
        print("Step 2.5 test PASSED - GitHub service works with mocks")
        sys.exit(0)
    print("Step 2.5 test FAILED - see logs/step_2_5_errors.log")
    sys.exit(1)
