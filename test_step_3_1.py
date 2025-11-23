# test_step_3_1.py
import sys

import customtkinter as ctk

from ui.main_window import MainWindow


def test_main_window_structure() -> bool:
    errors = []
    window = MainWindow()
    window.withdraw()

    try:
        if not isinstance(window.folder_entry, ctk.CTkEntry):
            errors.append("Folder entry widget is missing or wrong type.")
        if not isinstance(window.browse_button, ctk.CTkButton):
            errors.append("Browse button is missing.")
        if not isinstance(window.status_text, ctk.CTkTextbox):
            errors.append("Status text area is missing.")
        if not isinstance(window.progress_bar, ctk.CTkProgressBar):
            errors.append("Progress bar is missing.")
        if not window.description_entry:
            errors.append("Description textbox is missing.")
        if window.status_history:
            errors.append("Status history should start empty.")
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
    with open("logs/step_3_1_success.log", "w", encoding="utf-8") as f:
        f.write("Step 3.1: Main window structure verified.\n")


def log_errors(errors: list[str]) -> None:
    import os

    os.makedirs("logs", exist_ok=True)
    with open("logs/step_3_1_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 3.1 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(3, "3.1", True)
        print("Checklist updated for Step 3.1")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_main_window_structure()
    if success:
        print("Step 3.1 test PASSED - main window structure exists")
        sys.exit(0)
    print("Step 3.1 test FAILED - see logs/step_3_1_errors.log")
    sys.exit(1)
