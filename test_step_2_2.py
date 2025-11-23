# test_step_2_2.py
import os
import sys

from services.git_service import GitService


def test_git_service_structure() -> bool:
    errors = []
    service = GitService(os.getcwd())

    if not service.repo_path.exists():
        errors.append("GitService repo_path does not point to an existing folder.")

    expected_methods = [
        "initialize_repo",
        "create_gitkeep_files",
        "stage_all_files",
        "commit",
        "add_remote",
        "rename_branch",
        "push",
    ]

    for method_name in expected_methods:
        method = getattr(service, method_name, None)
        if method is None or not callable(method):
            errors.append(f"Missing or non-callable method: {method_name}")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_2_success.log", "w", encoding="utf-8") as f:
        f.write("Step 2.2: GitService structure verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_2_2_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 2.2 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(2, "2.2", True)
        print("Checklist updated for Step 2.2")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_git_service_structure()
    if success:
        print("Step 2.2 test PASSED - GitService stubs exist")
        sys.exit(0)
    print("Step 2.2 test FAILED - see logs/step_2_2_errors.log")
    sys.exit(1)
