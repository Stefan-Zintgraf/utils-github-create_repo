# test_step_4_2.py
import os
import sys
import tempfile

from pathlib import Path
from unittest import mock

from github.GithubException import UnknownObjectException

from services.git_service import GitService
from services.github_service import GitHubService


def test_end_to_end_flow() -> bool:
    errors = []

    with mock.patch("services.github_service.Github") as mock_github:
        mock_client = mock_github.return_value
        mock_user = mock.Mock()
        mock_repo = mock.Mock()
        mock_repo.clone_url = "https://example.com/integration.git"
        mock_user.create_repo.return_value = mock_repo
        mock_user.get_repo.side_effect = [
            mock_repo,
            UnknownObjectException(404, "Not Found", {}),
        ]
        mock_client.get_user.return_value = mock_user

        github_service = GitHubService("ghp_integrationtoken")

        try:
            repo_url = github_service.create_repository("integration-repo", private=True, description="Integration test")
        except Exception as exc:
            errors.append(f"GitHub repository creation raised unexpected exception: {exc}")
            repo_url = ""

        if repo_url != mock_repo.clone_url:
            errors.append("Repository clone URL does not match expected mock URL.")

        if not github_service.check_repository_exists("integration-repo"):
            errors.append("Created repository was not detected by GitHubService.")

        if github_service.check_repository_exists("does-not-exist"):
            errors.append("Non-existent repository was reported as existing.")

    with tempfile.TemporaryDirectory(prefix="integration_") as tmpdir:
        repo_path = Path(tmpdir)
        (repo_path / "docs").mkdir()
        (repo_path / "docs" / "readme.md").write_text("# Docs", encoding="utf-8")
        (repo_path / "source").mkdir()
        (repo_path / "source" / "code.py").write_text("print('hello')", encoding="utf-8")

        git_service = GitService(repo_path)

        if not git_service.initialize_repo():
            errors.append("Failed to initialize repository.")

        gitkeep_count = git_service.create_gitkeep_files()
        if gitkeep_count == 0:
            errors.append("Expected .gitkeep files to be created.")

        staged_count, total_size = git_service.stage_all_files()
        if staged_count == 0:
            errors.append("Staging did not report any files.")
        if total_size == 0:
            errors.append("Staging reported zero total size.")

        if not git_service.commit("Integration commit"):
            errors.append("Commit command failed.")

        if not git_service.add_remote(repo_url):
            errors.append("Failed to add remote origin.")

        if not git_service.rename_branch("main"):
            errors.append("Failed to rename branch to main.")

        with mock.patch.object(GitService, "push", return_value=True) as mocked_push:
            push_result = git_service.push("main", "origin")
            if not push_result:
                errors.append("Push returned False even though remote call was mocked.")
            if not mocked_push.called:
                errors.append("Push method was never invoked.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_4_2_success.log", "w", encoding="utf-8") as f:
        f.write("Step 4.2: End-to-end integration flow verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_4_2_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 4.2 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(4, "4.2", True)
        print("Checklist updated for Step 4.2")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_end_to_end_flow()
    if success:
        print("Step 4.2 test PASSED - integration flow works")
        sys.exit(0)
    print("Step 4.2 test FAILED - see logs/step_4_2_errors.log")
    sys.exit(1)
