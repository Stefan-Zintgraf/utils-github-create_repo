# test_step_5_1.py
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

from github.GithubException import GithubException

from services.git_service import GitService
from services.github_service import GitHubService
from utils.logger import LOG_FILE


def test_error_handling() -> bool:
    errors = []

    with tempfile.TemporaryDirectory(prefix="error_handling_") as tmpdir:
        repo_path = Path(tmpdir)

        with mock.patch("services.git_service.subprocess.run", side_effect=OSError("git command blocked")):
            service = GitService(repo_path)
            if service.initialize_repo():
                errors.append("initialize_repo should return False when git command fails.")

    if not os.path.isfile(LOG_FILE):
        errors.append("Expected application log file to exist after handling an error.")
    else:
        with open(LOG_FILE, encoding="utf-8") as f:
            content = f.read()
        if "Failed to run git command" not in content:
            errors.append("Application log does not mention the git command failure.")

    with mock.patch("services.github_service.Github") as mock_github:
        mock_client = mock_github.return_value
        mock_client.get_user.side_effect = GithubException(401, "Unauthorized", {})
        service = GitHubService("ghp_badtoken")
        if service.validate_token("ghp_badtoken"):
            errors.append("validate_token should return False when GitHubException is raised.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_5_1_success.log", "w", encoding="utf-8") as f:
        f.write("Step 5.1: Error handling verified via logs.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_5_1_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 5.1 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(5, "5.1", True)
        print("Checklist updated for Step 5.1")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_error_handling()
    if success:
        print("Step 5.1 test PASSED - error handling works")
        sys.exit(0)
    print("Step 5.1 test FAILED - see logs/step_5_1_errors.log")
    sys.exit(1)
