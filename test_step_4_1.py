# test_step_4_1.py
import sys
from unittest import mock

import main as main_module


def test_main_entry_point() -> bool:
    errors = []

    with mock.patch.object(main_module, "MainWindow") as mocked_window:
        main_module.main()

        if not mocked_window.called:
            errors.append("Main window was not instantiated by main().")

        instance = mocked_window.return_value
        if not instance.mainloop.called:
            errors.append("mainloop was not started.")

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    import os

    os.makedirs("logs", exist_ok=True)
    with open("logs/step_4_1_success.log", "w", encoding="utf-8") as f:
        f.write("Step 4.1: Main entry point verified.\n")


def log_errors(errors: list[str]) -> None:
    import os

    os.makedirs("logs", exist_ok=True)
    with open("logs/step_4_1_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 4.1 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(4, "4.1", True)
        print("Checklist updated for Step 4.1")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_main_entry_point()
    if success:
        print("Step 4.1 test PASSED - entry point works")
        sys.exit(0)
    print("Step 4.1 test FAILED - see logs/step_4_1_errors.log")
    sys.exit(1)
