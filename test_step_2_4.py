# test_step_2_4.py
import os
import subprocess
import sys
import tempfile

from pathlib import Path

from services.git_service import GitService


def test_git_operations() -> bool:
    errors = []
    with tempfile.TemporaryDirectory(prefix="git_operations_") as temp_dir:
        repo_path = Path(temp_dir)
        service = GitService(repo_path)

        (repo_path / "README.md").write_text("# Test Repo\n", encoding="utf-8")
        docs = repo_path / "docs"
        docs.mkdir()
        (docs / "guide.md").write_text("Guide content", encoding="utf-8")

        empty_dir = repo_path / "empty_folder"
        empty_dir.mkdir()

        if not service.initialize_repo():
            errors.append("Failed to initialize repository.")

        subprocess.run(["git", "config", "user.name", "GitHubRepoCreator"], cwd=repo_path)
        subprocess.run(["git", "config", "user.email", "repo@example.com"], cwd=repo_path)

        gitkeep_count = service.create_gitkeep_files()
        if gitkeep_count == 0:
            errors.append("Expected at least one .gitkeep file to be created.")

        staged_count, total_size = service.stage_all_files()
        if staged_count == 0:
            errors.append("Staging did not report any files.")
        if total_size == 0:
            errors.append("Stage reported zero total size.")

        if not service.commit("Initial commit"):
            errors.append("Commit failed, possibly due to git configuration.")

        if not service.add_remote("https://github.com/example/repo.git"):
            errors.append("Failed to add remote origin.")

        if not service.rename_branch("main"):
            errors.append("Failed to rename branch to main.")

        push_result = service.push("main", "origin")
        if not push_result:
            print("Push failed as expected (no accessible remote) but method returned False gracefully.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_4_success.log", "w", encoding="utf-8") as f:
        f.write("Step 2.4: Git operations methods verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_4_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 2.4 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(2, "2.4", True)
        print("Checklist updated for Step 2.4")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_git_operations()
    if success:
        print("Step 2.4 test PASSED - Git operations work")
        sys.exit(0)
    print("Step 2.4 test FAILED - see logs/step_2_4_errors.log")
    sys.exit(1)
