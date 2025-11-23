# test_step_1_3.py
import logging
import os
import sys

from utils.logger import LOG_DIR, LOG_FILE, configure_logger


def test_logging_setup() -> bool:
    errors = []

    os.makedirs(LOG_DIR, exist_ok=True)
    logger = configure_logger("test_step_1_3", logging.DEBUG)
    test_message = "Step 1.3 automated logging test entry"
    logger.debug(test_message)
    for handler in logger.handlers:
        handler.flush()

    if not os.path.isdir(LOG_DIR):
        errors.append("Logs directory is missing after configuring the logger.")
    if not os.path.isfile(LOG_FILE):
        errors.append("Log file was not created by the logger.")

    if errors:
        log_errors(errors)
        return False

    try:
        with open(LOG_FILE, encoding="utf-8") as f:
            log_content = f.read()
    except OSError as exc:
        errors.append(f"Could not read log file: {exc}")
        log_errors(errors)
        return False

    if test_message not in log_content:
        errors.append("Test message was not written to the log file.")
        log_errors(errors)
        return False

    log_success()
    update_checklist()
    return True


def log_success() -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_1_3_success.log", "w", encoding="utf-8") as f:
        f.write("Step 1.3: Logging directory and utility verified.\n")


def log_errors(errors: list[str]) -> None:
    os.makedirs("logs", exist_ok=True)
    with open("logs/step_1_3_errors.log", "w", encoding="utf-8") as f:
        f.write("Step 1.3 failed due to the following issues:\n")
        for msg in errors:
            f.write(f"{msg}\n")


def update_checklist() -> None:
    try:
        from update_checklist import update_step

        update_step(1, "1.3", True)
        print("Checklist updated for Step 1.3")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: could not update checklist: {exc}")


if __name__ == "__main__":
    success = test_logging_setup()
    if success:
        print("Step 1.3 test PASSED - logging utility working")
        sys.exit(0)
    print("Step 1.3 test FAILED - see logs/step_1_3_errors.log")
    sys.exit(1)
