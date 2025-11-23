"""GUI window definition for GitHub Repository Creator."""

from __future__ import annotations

import queue
import threading
import time

import customtkinter as ctk

from utils.logger import configure_logger


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title("GitHub Repository Creator")
        self.geometry("800x700")

        self.folder_path_var = ctk.StringVar()
        self.status_history: list[tuple[str, bool]] = []
        self.progress_value = 0
        self._operation_thread: threading.Thread | None = None
        self._operation_complete_event = threading.Event()
        self._status_queue: queue.Queue[tuple[str, bool]] = queue.Queue()
        self._progress_queue: queue.Queue[int] = queue.Queue()
        self.logger = configure_logger("ui_main_window")

        self._setup_ui()
        self.after(50, self._process_queue)

    def _setup_ui(self) -> None:
        """Create UI components."""
        self.folder_entry = ctk.CTkEntry(self, placeholder_text="Source Folder Path", textvariable=self.folder_path_var)
        self.folder_entry.pack(pady=8, padx=12, fill="x")

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.on_browse_clicked)
        self.browse_button.pack(pady=4, padx=12)

        self.token_entry = ctk.CTkEntry(self, placeholder_text="GitHub Token", show="*")
        self.token_entry.pack(pady=4, padx=12, fill="x")

        self.repo_entry = ctk.CTkEntry(self, placeholder_text="Repository Name")
        self.repo_entry.pack(pady=4, padx=12, fill="x")

        self.description_entry = ctk.CTkTextbox(self, width=400, height=80)
        self.description_entry.pack(pady=4, padx=12, fill="x")

        self.commit_entry = ctk.CTkEntry(self, placeholder_text="Initial Commit Message")
        self.commit_entry.pack(pady=4, padx=12, fill="x")

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=4, padx=12, fill="x")

        self.status_text = ctk.CTkTextbox(self, width=400, height=120)
        self.status_text.configure(state="disabled")
        self.status_text.pack(pady=8, padx=12, fill="both", expand=True)

        action_frame = ctk.CTkFrame(self)
        action_frame.pack(pady=8, padx=12, fill="x")

        self.create_button = ctk.CTkButton(action_frame, text="Create Repository & Push", command=self.on_create_clicked)
        self.create_button.pack(side="left", expand=True, padx=4)
        self.clear_button = ctk.CTkButton(action_frame, text="Clear", command=self.on_clear_clicked)
        self.clear_button.pack(side="left", expand=True, padx=4)
        self.exit_button = ctk.CTkButton(action_frame, text="Exit", command=self.destroy)
        self.exit_button.pack(side="left", expand=True, padx=4)

    def on_browse_clicked(self) -> None:
        """Handle browse button click (stub)."""
        self.update_status("Browse dialog opened (placeholder).")

    def on_create_clicked(self) -> None:
        """Handle create button click."""
        if self._operation_thread and self._operation_thread.is_alive():
            self.update_status("A creation task is already running.", error=True)
            return

        self._operation_complete_event.clear()
        self.update_status("Create operation started.")
        self.update_progress(0)
        self.logger.info("Starting background create operations")
        self._operation_thread = threading.Thread(target=self._perform_create_operations, daemon=True)
        self._operation_thread.start()

    def on_clear_clicked(self) -> None:
        """Reset all form fields."""
        self.folder_entry.delete(0, "end")
        self.token_entry.delete(0, "end")
        self.repo_entry.delete(0, "end")
        self.description_entry.delete("1.0", "end")
        self.commit_entry.delete(0, "end")
        self.update_progress(0)
        self.update_status("Fields cleared.")

    def update_status(self, message: str, error: bool = False) -> None:
        """Append a message to the status log."""
        self.status_history.append((message, error))
        self._append_status(message, error)

    def _append_status(self, message: str, error: bool) -> None:
        self.status_text.configure(state="normal")
        prefix = "[ERROR]" if error else "[INFO]"
        self.status_text.insert("end", f"{prefix} {message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")

    def update_progress(self, value: int | None = None) -> None:
        """Adjust progress bar value."""
        if value is None:
            self.progress_bar.set(0)
            self.progress_value = 0
            return

        normalized = max(0, min(100, value))
        self.progress_value = normalized
        self.progress_bar.set(normalized / 100)

    def _perform_create_operations(self) -> None:
        steps = [
            (20, "Scanning folders..."),
            (40, "Creating .gitkeep files..."),
            (60, "Staging files..."),
            (80, "Committing changes..."),
            (95, "Configuring remote..."),
        ]
        try:
            for value, message in steps:
                self._enqueue_status(message)
                self._enqueue_progress(value)
                time.sleep(0.05)

            self._enqueue_status("Background create operation completed.")
            self._enqueue_progress(100)
        except Exception:
            self.logger.exception("Background create operation failed")
            self._enqueue_status("Background create operation failed.", error=True)
            self._enqueue_progress(0)
        finally:
            self._operation_complete_event.set()
            self._operation_thread = None

    def _enqueue_status(self, message: str, error: bool = False) -> None:
        self._status_queue.put((message, error))

    def _enqueue_progress(self, value: int | None) -> None:
        self._progress_queue.put(value if value is not None else 0)

    def _process_queue(self) -> None:
        while not self._status_queue.empty():
            message, error = self._status_queue.get()
            self.update_status(message, error)

        while not self._progress_queue.empty():
            value = self._progress_queue.get()
            self.update_progress(value)

        self.after(50, self._process_queue)
