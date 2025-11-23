# test_step_2_3.py
import os
import sys
import tempfile

from pathlib import Path

from services.git_service import GitService


def test_gitkeep_generation() -> bool:
    errors = []
    with tempfile.TemporaryDirectory(prefix="gitkeep_test_") as temp_dir:
        repo_path = Path(temp_dir)
        empty_dir = repo_path / "empty_folder"
        nested_dir = empty_dir / "nested_empty"
        nested_dir.mkdir(parents=True)

        filled_dir = repo_path / "filled_folder"
        filled_dir.mkdir()
        (filled_dir / "file.txt").write_text("payload", encoding="utf-8")

        git_dir = repo_path / ".git"
        git_dir.mkdir()
        (git_dir / "config").write_text("", encoding="utf-8")

        service = GitService(repo_path)
        created = service.create_gitkeep_files()

        if created < 2:
            errors.append("Expected at least two .gitkeep files in empty directories.")

        for target in (empty_dir, nested_dir):
            gitkeep = target / ".gitkeep"
            if not gitkeep.exists():
                errors.append(f".gitkeep was not created in {target}")

        if (filled_dir / ".gitkeep").exists():
            errors.append("Filled directory should not receive a .gitkeep.")

        if (git_dir / ".gitkeep").exists():
            errors.append(".gitkeep must not be placed inside .git.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_3_success.log", "w", encoding="utf-8") as f:
        f.write("Step 2.3: .gitkeep generation verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_3_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 2.3 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(2, "2.3", True)
        print("Checklist updated for Step 2.3")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_gitkeep_generation()
    if success:
        print("Step 2.3 test PASSED - .gitkeep files created as expected")
        sys.exit(0)
    print("Step 2.3 test FAILED - see logs/step_2_3_errors.log")
    sys.exit(1)
