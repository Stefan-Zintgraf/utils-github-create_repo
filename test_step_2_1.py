# test_step_2_1.py
import os
import sys
import tempfile
from pathlib import Path

from services.validation_service import ValidationService


def test_validation_service() -> bool:
    errors = []

    with tempfile.TemporaryDirectory(prefix="validation_good_") as tmp:
        ok, message = ValidationService.validate_folder_path(tmp)
        if not ok:
            errors.append(f"Temporary directory should be valid: {message}")

    with tempfile.TemporaryDirectory(prefix="validation_git_") as tmp_git:
        Path(tmp_git, ".git").mkdir()
        ok, message = ValidationService.validate_folder_path(tmp_git)
        if ok:
            errors.append("Folder with .git should not be considered valid.")

    invalid_path = os.path.join("nonexistent", "folder")
    ok, message = ValidationService.validate_folder_path(invalid_path)
    if ok:
        errors.append("Validation wrongly accepted a non-existent folder path.")

    ok, message = ValidationService.validate_repository_name("valid-repo_name")
    if not ok:
        errors.append(f"Valid repository name rejected: {message}")

    ok, message = ValidationService.validate_repository_name("invalid repo name!")
    if ok:
        errors.append("Repository name with spaces/punctuation was incorrectly accepted.")

    ok, message = ValidationService.validate_token("ghp_abcdefghijklmnopqrstuvwxyz1234567890")
    if not ok:
        errors.append(f"Valid token rejected: {message}")

    ok, message = ValidationService.validate_token("badtoken")
    if ok:
        errors.append("Invalid token format was incorrectly accepted.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_1_success.log", "w", encoding="utf-8") as f:
        f.write("Step 2.1: Validation service verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_1_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 2.1 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(2, "2.1", True)
        print("Checklist updated for Step 2.1")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_validation_service()
    if success:
        print("Step 2.1 test PASSED - Validation helpers work")
        sys.exit(0)
    print("Step 2.1 test FAILED - see logs/step_2_1_errors.log")
    sys.exit(1)
