# test_step_3_2.py
import sys

from ui.main_window import MainWindow


def test_event_handlers() -> bool:
    errors = []
    window = MainWindow()
    window.withdraw()

    try:
        window.on_browse_clicked()
        window.on_create_clicked()
        window.on_clear_clicked()

        if not window.status_history:
            errors.append("Status history did not record any updates.")
        if window.progress_value != 0:
            errors.append("Progress bar did not reset after clear.")
    finally:
        window.destroy()

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    import os

    os.makedirs("logs", exist_ok=True)
    with open("logs/step_3_2_success.log", "w", encoding="utf-8") as f:
        f.write("Step 3.2: UI event handlers verified.\n")


def log_errors(errors: list[str]) -> None:
    import os

    os.makedirs("logs", exist_ok=True)
    with open("logs/step_3_2_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 3.2 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(3, "3.2", True)
        print("Checklist updated for Step 3.2")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_event_handlers()
    if success:
        print("Step 3.2 test PASSED - UI handlers invoked")
        sys.exit(0)
    print("Step 3.2 test FAILED - see logs/step_3_2_errors.log")
    sys.exit(1)
