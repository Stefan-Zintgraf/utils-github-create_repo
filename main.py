# main.py
"""GitHub Repository Creator - Main Entry Point."""

from ui.main_window import MainWindow


def main() -> None:
    """Launch the main application window."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()

