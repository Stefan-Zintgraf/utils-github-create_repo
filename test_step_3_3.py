# test_step_3_3.py
import os
import sys

from ui.main_window import MainWindow


def test_background_threading() -> bool:
    errors = []
    window = MainWindow()
    window.withdraw()

    try:
        window.on_create_clicked()
        if not window._operation_thread:
            errors.append("Background thread failed to start.")
        else:
            completed = window._operation_complete_event.wait(timeout=5)
            window.update()
            if not completed:
                errors.append("Background thread did not signal completion in time.")
            if window.progress_value != 100:
                errors.append("Progress did not reach 100.")
            if not any("Background create operation completed." in msg for msg, _ in window.status_history):
                errors.append("Completion message missing from status history.")
    finally:
        window.destroy()

    if errors:
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_3_3_success.log", "w", encoding="utf-8") as f:
        f.write("Step 3.3: Background threading verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_3_3_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 3.3 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(3, "3.3", True)
        print("Checklist updated for Step 3.3")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_background_threading()
    if success:
        print("Step 3.3 test PASSED - background threading works")
        sys.exit(0)
    print("Step 3.3 test FAILED - see logs/step_3_3_errors.log")
    sys.exit(1)
