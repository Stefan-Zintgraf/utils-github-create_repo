# test_step_1_2.py
import os
import sys


def test_requirements():
    errors = []
    expected_deps = {
        "customtkinter>=5.2.0",
        "PyGithub>=2.1.1",
        "GitPython>=3.1.40",
        "requests>=2.31.0",
    }

    if not os.path.isfile("requirements.txt"):
        errors.append("Missing requirements.txt")
        log_errors(errors)
        return False

    with open("requirements.txt", encoding="utf-8") as f:
        current = {line.strip() for line in f if line.strip()}

    missing = expected_deps - current
    extra = current - expected_deps

    if missing:
        errors.append("Missing dependencies:")
        errors.extend(f"  - {dep}" for dep in sorted(missing))

    if extra:
        errors.append("Unexpected lines in requirements.txt:")
        errors.extend(f"  - {line}" for line in sorted(extra))

    if errors:
        log_errors(errors)
        return False

    log_success(expected_deps)
    update_checklist()
    return True


def log_success(deps):
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_1_2_success.log", "w", encoding="utf-8") as f:
        f.write("Step 1.2: Requirements file matches the specification.\n")
        f.write("Dependencies declared:\n")
        for dep in sorted(deps):
            f.write(f"  - {dep}\n")


def log_errors(errors):
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_1_2_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 1.2 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist():
    try:
        from update_checklist import update_step
        update_step(1, "1.2", True)
        print("Checklist updated for Step 1.2")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_requirements()
    if success:
        print("Step 1.2 test PASSED - requirements.txt is correct")
        sys.exit(0)
    print("Step 1.2 test FAILED - see logs/step_1_2_errors.log")
    sys.exit(1)
