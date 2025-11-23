# test_step_5_2.py
import os
import sys


def test_gitignore_contents() -> bool:
    errors = []
    required_patterns = [
        "__pycache__/",
        ".env",
        ".env.*",
        "logs/",
        ".DS_Store",
        "github_token.txt",
        "p*_s*/",
    ]

    if not os.path.isfile(".gitignore"):
        errors.append(".gitignore file is missing.")
    else:
        with open(".gitignore", encoding="utf-8") as f:
            content = f.read()

        for pattern in required_patterns:
            if pattern not in content:
                errors.append(f".gitignore missing required pattern: {pattern}")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_5_2_success.log", "w", encoding="utf-8") as f:
        f.write("Step 5.2: .gitignore content verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_5_2_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 5.2 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(5, "5.2", True)
        print("Checklist updated for Step 5.2")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_gitignore_contents()
    if success:
        print("Step 5.2 test PASSED - .gitignore content is complete")
        sys.exit(0)
    print("Step 5.2 test FAILED - see logs/step_5_2_errors.log")
    sys.exit(1)
