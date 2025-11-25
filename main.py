"""
GitHub Repository Creator - Main Entry Point

A GUI application for creating GitHub repositories from local Windows folders.
"""

import sys
import customtkinter
from ui.main_window import MainWindow

def main():
    """Main entry point for the application."""
    # Set appearance mode and color theme
    customtkinter.set_appearance_mode("system")  # Modes: "System" (default), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
    
    # Create and run the main window
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()

