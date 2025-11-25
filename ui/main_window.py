"""
Main window UI for GitHub Repository Creator.

Provides the GUI interface using CustomTkinter.
"""

import customtkinter
import tkinter.filedialog
import threading
from typing import Optional

from services.validation_service import (
    validate_folder_path,
    validate_repository_name,
    validate_token
)
from services.git_service import GitService
from services.github_service import GitHubService
from utils.logger import setup_logger
from utils.config import load_config, save_config


class MainWindow(customtkinter.CTk):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window and all UI components."""
        super().__init__()
        
        # Window configuration
        self.title("GitHub Repository Creator")
        self.geometry("800x600")
        self.minsize(600, 400)  # Minimum window size
        self.resizable(True, True)
        
        # Variables
        self.folder_path_var = customtkinter.StringVar()
        self.username_var = customtkinter.StringVar()
        self.token_var = customtkinter.StringVar()
        self.repo_name_var = customtkinter.StringVar()
        self.visibility_var = customtkinter.StringVar(value="private")
        self.description_var = customtkinter.StringVar()
        self.commit_message_var = customtkinter.StringVar(
            value="Initial commit: add all files and subfolders"
        )
        
        # Logger
        self.logger = setup_logger(__name__)
        
        # Processing state
        self.is_processing = False
        
        # Create UI components
        self._create_widgets()
        
        # Load saved configuration (prefill fields)
        self._load_config()
        
        # Bind to save config when values change
        self._setup_config_autosave()
        
        # Center window on screen
        self._center_window()
        
        # Handle window close to save config
        self.protocol("WM_DELETE_WINDOW", self.on_exit_clicked)
    
    def _center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Create scrollable frame for main content
        scrollable_frame = customtkinter.CTkScrollableFrame(self)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Main container with padding (inside scrollable frame)
        main_frame = customtkinter.CTkFrame(scrollable_frame)
        main_frame.pack(fill="both", expand=True)
        
        # Header Section
        header_label = customtkinter.CTkLabel(
            main_frame,
            text="Create GitHub Repository",
            font=customtkinter.CTkFont(size=24, weight="bold")
        )
        header_label.pack(pady=(0, 5))
        
        subtitle_label = customtkinter.CTkLabel(
            main_frame,
            text="Migrate local folder to GitHub",
            font=customtkinter.CTkFont(size=12)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Source Folder Section
        folder_frame = customtkinter.CTkFrame(main_frame)
        folder_frame.pack(fill="x", pady=10)
        
        folder_label_frame = customtkinter.CTkFrame(folder_frame)
        folder_label_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        folder_label = customtkinter.CTkLabel(
            folder_label_frame,
            text="Source Folder Path",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        folder_label.pack(side="left")
        
        self._create_help_button(
            folder_label_frame,
            "Source Folder Path",
            "Select the local folder you want to migrate to GitHub.\n\n"
            "Example: C:\\Users\\YourName\\Documents\\MyProject\n\n"
            "The folder should contain the files and subfolders you want to upload.\n"
            "Empty folders will be preserved using .gitkeep files."
        )
        
        folder_entry_frame = customtkinter.CTkFrame(folder_frame)
        folder_entry_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.folder_entry = customtkinter.CTkEntry(
            folder_entry_frame,
            textvariable=self.folder_path_var,
            placeholder_text="Select a folder...",
            width=500
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_button = customtkinter.CTkButton(
            folder_entry_frame,
            text="Browse",
            command=self.on_browse_clicked,
            width=100
        )
        self.browse_button.pack(side="right")
        
        # GitHub Authentication Section
        auth_frame = customtkinter.CTkFrame(main_frame)
        auth_frame.pack(fill="x", pady=10)
        
        auth_label = customtkinter.CTkLabel(
            auth_frame,
            text="GitHub Authentication",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        auth_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        username_label_frame = customtkinter.CTkFrame(auth_frame)
        username_label_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        username_label = customtkinter.CTkLabel(
            username_label_frame,
            text="Username:"
        )
        username_label.pack(side="left")
        
        self._create_help_button(
            username_label_frame,
            "GitHub Username",
            "Enter your GitHub username (not email).\n\n"
            "Example: octocat\n\n"
            "This is the username you use to log in to GitHub.\n"
            "It's the part before @ in your GitHub profile URL."
        )
        
        self.username_entry = customtkinter.CTkEntry(
            auth_frame,
            textvariable=self.username_var,
            placeholder_text="GitHub username",
            width=400
        )
        self.username_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        token_label_frame = customtkinter.CTkFrame(auth_frame)
        token_label_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        token_label = customtkinter.CTkLabel(
            token_label_frame,
            text="Personal Access Token:"
        )
        token_label.pack(side="left")
        
        self._create_help_button(
            token_label_frame,
            "Personal Access Token",
            "Enter your GitHub Personal Access Token (PAT).\n\n"
            "Format examples:\n"
            "• Classic token: ghp_1234567890abcdef1234567890abcdef12345678\n"
            "• Fine-grained: github_pat_1234567890abcdef1234567890abcdef...\n\n"
            "To create a token:\n"
            "1. Go to GitHub Settings > Developer settings > Personal access tokens\n"
            "2. Generate new token (classic) or fine-grained token\n"
            "3. Select 'repo' scope for repository creation\n"
            "4. Copy the token immediately (it won't be shown again)\n\n"
            "⚠️ Security: The token will NOT be saved to disk for security reasons."
        )
        
        self.token_entry = customtkinter.CTkEntry(
            auth_frame,
            textvariable=self.token_var,
            placeholder_text="ghp_... or github_pat_...",
            show="*",
            width=400
        )
        self.token_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        token_info = customtkinter.CTkLabel(
            auth_frame,
            text="Use Personal Access Token (recommended)",
            font=customtkinter.CTkFont(size=10),
            text_color="gray"
        )
        token_info.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Repository Details Section
        repo_frame = customtkinter.CTkFrame(main_frame)
        repo_frame.pack(fill="x", pady=10)
        
        repo_label = customtkinter.CTkLabel(
            repo_frame,
            text="Repository Details",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        repo_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        repo_name_label_frame = customtkinter.CTkFrame(repo_frame)
        repo_name_label_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        repo_name_label = customtkinter.CTkLabel(
            repo_name_label_frame,
            text="Repository Name:"
        )
        repo_name_label.pack(side="left")
        
        self._create_help_button(
            repo_name_label_frame,
            "Repository Name",
            "Enter the name for your new GitHub repository.\n\n"
            "Examples:\n"
            "• my-awesome-project\n"
            "• python_utils\n"
            "• test-repo-123\n\n"
            "Rules:\n"
            "• 1-100 characters\n"
            "• Only letters, numbers, hyphens (-), underscores (_), and periods (.)\n"
            "• Cannot start or end with a period\n"
            "• Cannot contain consecutive periods\n"
            "• Must be unique (not already exist in your account)"
        )
        
        self.repo_name_entry = customtkinter.CTkEntry(
            repo_frame,
            textvariable=self.repo_name_var,
            placeholder_text="my-repository",
            width=400
        )
        self.repo_name_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        visibility_label_frame = customtkinter.CTkFrame(repo_frame)
        visibility_label_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        visibility_label = customtkinter.CTkLabel(
            visibility_label_frame,
            text="Visibility:"
        )
        visibility_label.pack(side="left")
        
        self._create_help_button(
            visibility_label_frame,
            "Repository Visibility",
            "Choose whether your repository is Private or Public.\n\n"
            "• Private: Only you (and collaborators you add) can see and access the repository\n"
            "• Public: Anyone on the internet can view the repository\n\n"
            "Default: Private (recommended for most use cases)\n\n"
            "You can change this later in the repository settings on GitHub."
        )
        
        visibility_frame = customtkinter.CTkFrame(repo_frame)
        visibility_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.private_radio = customtkinter.CTkRadioButton(
            visibility_frame,
            text="Private",
            variable=self.visibility_var,
            value="private"
        )
        self.private_radio.pack(side="left", padx=(0, 20))
        
        self.public_radio = customtkinter.CTkRadioButton(
            visibility_frame,
            text="Public",
            variable=self.visibility_var,
            value="public"
        )
        self.public_radio.pack(side="left")
        
        description_label_frame = customtkinter.CTkFrame(repo_frame)
        description_label_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        description_label = customtkinter.CTkLabel(
            description_label_frame,
            text="Description (optional):"
        )
        description_label.pack(side="left")
        
        self._create_help_button(
            description_label_frame,
            "Repository Description",
            "Enter an optional description for your repository.\n\n"
            "Examples:\n"
            "• \"A collection of utility scripts for data processing\"\n"
            "• \"My personal project for learning Python\"\n"
            "• \"Custom indicators for NinjaTrader 8\"\n\n"
            "This description will appear on your repository's main page on GitHub.\n"
            "It helps others understand what the repository is about.\n\n"
            "This field is optional - you can leave it empty."
        )
        
        self.description_entry = customtkinter.CTkEntry(
            repo_frame,
            textvariable=self.description_var,
            placeholder_text="Repository description",
            width=400
        )
        self.description_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Commit Message Section
        commit_frame = customtkinter.CTkFrame(main_frame)
        commit_frame.pack(fill="x", pady=10)
        
        commit_label_frame = customtkinter.CTkFrame(commit_frame)
        commit_label_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        commit_label = customtkinter.CTkLabel(
            commit_label_frame,
            text="Initial Commit Message",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        commit_label.pack(side="left")
        
        self._create_help_button(
            commit_label_frame,
            "Initial Commit Message",
            "Enter the message for the initial commit.\n\n"
            "Examples:\n"
            "• \"Initial commit: add all files and subfolders\"\n"
            "• \"First commit\"\n"
            "• \"Initial repository setup\"\n\n"
            "This message will be used for the first commit when pushing to GitHub.\n"
            "It describes what this commit contains.\n\n"
            "Default: \"Initial commit: add all files and subfolders\""
        )
        
        self.commit_message_entry = customtkinter.CTkEntry(
            commit_frame,
            textvariable=self.commit_message_var,
            width=400
        )
        self.commit_message_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # Progress Section
        progress_frame = customtkinter.CTkFrame(main_frame)
        progress_frame.pack(fill="both", expand=True, pady=10)
        
        progress_label = customtkinter.CTkLabel(
            progress_frame,
            text="Status",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        progress_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.progress_bar = customtkinter.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(5, 10))
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()  # Hide initially
        
        self.status_text = customtkinter.CTkTextbox(
            progress_frame,
            height=150,
            wrap="word"
        )
        self.status_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Action Buttons Section
        button_frame = customtkinter.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.create_button = customtkinter.CTkButton(
            button_frame,
            text="Create Repository & Push",
            command=self.on_create_clicked,
            width=200,
            height=40,
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        self.create_button.pack(side="left", padx=10, pady=10)
        
        self.clear_button = customtkinter.CTkButton(
            button_frame,
            text="Clear",
            command=self.on_clear_clicked,
            width=100
        )
        self.clear_button.pack(side="left", padx=10, pady=10)
        
        self.exit_button = customtkinter.CTkButton(
            button_frame,
            text="Exit",
            command=self.on_exit_clicked,
            width=100
        )
        self.exit_button.pack(side="right", padx=10, pady=10)
    
    def on_browse_clicked(self):
        """Handle browse button click."""
        folder = tkinter.filedialog.askdirectory(title="Select Folder to Migrate")
        if folder:
            self.folder_path_var.set(folder)
            self.update_status(f"Selected folder: {folder}")
            # Save config when folder is selected
            self._save_config()
    
    def on_create_clicked(self):
        """Handle create repository button click."""
        if self.is_processing:
            return
        
        # Validate inputs
        folder_path = self.folder_path_var.get().strip()
        token = self.token_var.get().strip()
        repo_name = self.repo_name_var.get().strip()
        commit_message = self.commit_message_var.get().strip()
        
        # Validate folder path
        valid, msg = validate_folder_path(folder_path)
        if not valid:
            self.update_status(f"Error: {msg}", error=True)
            return
        
        # Validate repository name
        valid, msg = validate_repository_name(repo_name)
        if not valid:
            self.update_status(f"Error: {msg}", error=True)
            return
        
        # Validate token
        valid, msg = validate_token(token)
        if not valid:
            self.update_status(f"Error: {msg}", error=True)
            return
        
        # Validate commit message
        if not commit_message:
            self.update_status("Error: Commit message cannot be empty", error=True)
            return
        
        # Disable UI
        self._set_processing_state(True)
        
        # Start background thread
        thread = threading.Thread(
            target=self._create_repository_workflow,
            args=(folder_path, token, repo_name, commit_message),
            daemon=True
        )
        thread.start()
    
    def _create_repository_workflow(
        self,
        folder_path: str,
        token: str,
        repo_name: str,
        commit_message: str
    ):
        """Execute the full repository creation workflow in background thread."""
        try:
            self._update_status_thread_safe("Starting repository creation process...")
            
            # Step 1: Create GitHub repository
            self._update_status_thread_safe("Creating GitHub repository...")
            github_service = GitHubService(token)
            
            # Validate token
            if not github_service.validate_token():
                self._update_status_thread_safe("Error: Invalid GitHub token", error=True)
                self._set_processing_state(False)
                return
            
            # Create repository
            is_private = self.visibility_var.get() == "private"
            description = self.description_var.get().strip()
            repo_url = github_service.create_repository(
                name=repo_name,
                private=is_private,
                description=description
            )
            self._update_status_thread_safe(f"✓ GitHub repository created: {repo_name}")
            
            # Step 2: Initialize Git repository
            self._update_status_thread_safe("Initializing Git repository...")
            git_service = GitService(folder_path)
            
            if not git_service.initialize_repo():
                self._update_status_thread_safe("Error: Failed to initialize Git repository", error=True)
                self._set_processing_state(False)
                return
            self._update_status_thread_safe("✓ Git repository initialized")
            
            # Step 3: Create .gitkeep files for empty folders
            self._update_status_thread_safe("Creating .gitkeep files for empty folders...")
            gitkeep_count = git_service.create_gitkeep_files()
            if gitkeep_count > 0:
                self._update_status_thread_safe(f"✓ Created {gitkeep_count} .gitkeep file(s)")
            else:
                self._update_status_thread_safe("✓ No empty folders found")
            
            # Step 4: Stage all files
            self._update_status_thread_safe("Staging files...")
            file_count, total_size = git_service.stage_all_files()
            size_mb = total_size / (1024 * 1024)
            self._update_status_thread_safe(f"✓ Staged {file_count} file(s) ({size_mb:.2f} MB)")
            
            # Step 5: Create commit
            self._update_status_thread_safe("Creating commit...")
            if not git_service.commit(commit_message):
                self._update_status_thread_safe("Error: Failed to create commit", error=True)
                self._set_processing_state(False)
                return
            self._update_status_thread_safe("✓ Commit created")
            
            # Step 6: Add remote
            self._update_status_thread_safe("Adding remote repository...")
            if not git_service.add_remote(repo_url):
                self._update_status_thread_safe("Error: Failed to add remote", error=True)
                self._set_processing_state(False)
                return
            self._update_status_thread_safe("✓ Remote added")
            
            # Step 7: Rename branch to main
            self._update_status_thread_safe("Renaming branch to 'main'...")
            if not git_service.rename_branch("main"):
                self._update_status_thread_safe("Warning: Could not rename branch (may already be 'main')")
            else:
                self._update_status_thread_safe("✓ Branch renamed to 'main'")
            
            # Step 8: Push to GitHub
            self._update_status_thread_safe("Pushing to GitHub...")
            if not git_service.push("main", "origin"):
                self._update_status_thread_safe("Error: Failed to push to GitHub", error=True)
                self._set_processing_state(False)
                return
            self._update_status_thread_safe("✓ Pushed to GitHub")
            
            # Success!
            self._update_status_thread_safe("")
            self._update_status_thread_safe("=" * 50)
            self._update_status_thread_safe("✓ Repository creation completed successfully!")
            self._update_status_thread_safe(f"Repository URL: {repo_url}")
            self._update_status_thread_safe("=" * 50)
            
            # Hide progress bar
            self.after(0, lambda: self.progress_bar.pack_forget())
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self._update_status_thread_safe(error_msg, error=True)
            self.logger.error(f"Repository creation failed: {str(e)}", exc_info=True)
        finally:
            self._set_processing_state(False)
    
    def _set_processing_state(self, processing: bool):
        """Set the processing state and update UI accordingly."""
        self.is_processing = processing
        self.after(0, lambda: self._update_ui_processing_state(processing))
    
    def _update_ui_processing_state(self, processing: bool):
        """Update UI elements based on processing state (called from main thread)."""
        if processing:
            self.create_button.configure(text="Processing...", state="disabled")
            self.browse_button.configure(state="disabled")
            self.username_entry.configure(state="disabled")
            self.token_entry.configure(state="disabled")
            self.repo_name_entry.configure(state="disabled")
            self.description_entry.configure(state="disabled")
            self.commit_message_entry.configure(state="disabled")
            self.private_radio.configure(state="disabled")
            self.public_radio.configure(state="disabled")
            self.progress_bar.pack(fill="x", padx=10, pady=(5, 10), before=self.status_text)
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
        else:
            self.create_button.configure(text="Create Repository & Push", state="normal")
            self.browse_button.configure(state="normal")
            self.username_entry.configure(state="normal")
            self.token_entry.configure(state="normal")
            self.repo_name_entry.configure(state="normal")
            self.description_entry.configure(state="normal")
            self.commit_message_entry.configure(state="normal")
            self.private_radio.configure(state="normal")
            self.public_radio.configure(state="normal")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
    
    def _update_status_thread_safe(self, message: str, error: bool = False):
        """Update status from background thread (thread-safe)."""
        self.after(0, lambda: self.update_status(message, error))
    
    def on_clear_clicked(self):
        """Handle clear button click."""
        self.folder_path_var.set("")
        self.username_var.set("")
        self.token_var.set("")
        self.repo_name_var.set("")
        self.visibility_var.set("private")
        self.description_var.set("")
        self.commit_message_var.set("Initial commit: add all files and subfolders")
        self.status_text.delete("1.0", "end")
        self.progress_bar.pack_forget()
        self.update_status("Fields cleared")
        # Save cleared config
        self._save_config()
    
    def on_exit_clicked(self):
        """Handle exit button click."""
        # Save configuration before exiting
        self._save_config()
        self.destroy()
    
    def update_status(self, message: str, error: bool = False):
        """
        Update status text area.
        
        Args:
            message: Status message to display
            error: If True, display as error (red text)
        """
        self.status_text.insert("end", f"{message}\n")
        # Auto-scroll to bottom
        self.status_text.see("end")
        self.update()
    
    def update_progress(self, value: Optional[int] = None):
        """
        Update progress bar.
        
        Args:
            value: Progress value (0-100) or None for indeterminate
        """
        if value is not None:
            # Determinate progress
            self.progress_bar.pack(fill="x", padx=10, pady=(5, 10), before=self.status_text)
            self.progress_bar.set(value / 100.0)
        else:
            # Indeterminate progress - show and start animation
            self.progress_bar.pack(fill="x", padx=10, pady=(5, 10), before=self.status_text)
            self.progress_bar.configure(mode="indeterminate")
            self.progress_bar.start()
        self.update()
    
    def _create_help_button(self, parent, title: str, message: str):
        """
        Create a help/info button next to a label.
        
        Args:
            parent: Parent widget
            title: Title for the help dialog
            message: Help message to display
        """
        help_button = customtkinter.CTkButton(
            parent,
            text="?",
            width=25,
            height=25,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            command=lambda: self._show_help_dialog(title, message)
        )
        help_button.pack(side="right", padx=(5, 0))
    
    def _show_help_dialog(self, title: str, message: str):
        """
        Show a help dialog with information.
        
        Args:
            title: Dialog title
            message: Help message
        """
        dialog = customtkinter.CTkToplevel(self)
        dialog.title(f"Help: {title}")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog on parent window
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Title
        title_label = customtkinter.CTkLabel(
            dialog,
            text=title,
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(20, 10), padx=20)
        
        # Message text
        message_text = customtkinter.CTkTextbox(
            dialog,
            wrap="word",
            height=250
        )
        message_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        message_text.insert("1.0", message)
        message_text.configure(state="disabled")
        
        # Close button
        close_button = customtkinter.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=100
        )
        close_button.pack(pady=(0, 20))
    
    def _load_config(self):
        """Load saved configuration and prefill fields."""
        config = load_config()
        
        if 'folder_path' in config:
            self.folder_path_var.set(config.get('folder_path', ''))
        
        if 'username' in config:
            self.username_var.set(config.get('username', ''))
        
        # Note: PAT is NOT loaded from config (security requirement)
        
        if 'repo_name' in config:
            self.repo_name_var.set(config.get('repo_name', ''))
        
        if 'visibility' in config:
            self.visibility_var.set(config.get('visibility', 'private'))
        
        if 'description' in config:
            self.description_var.set(config.get('description', ''))
        
        if 'commit_message' in config:
            self.commit_message_var.set(config.get('commit_message', 'Initial commit: add all files and subfolders'))
    
    def _save_config(self):
        """Save current field values to configuration file (excluding PAT)."""
        config = {
            'folder_path': self.folder_path_var.get().strip(),
            'username': self.username_var.get().strip(),
            # PAT is explicitly NOT saved (security requirement)
            'repo_name': self.repo_name_var.get().strip(),
            'visibility': self.visibility_var.get(),
            'description': self.description_var.get().strip(),
            'commit_message': self.commit_message_var.get().strip()
        }
        save_config(config)
    
    def _setup_config_autosave(self):
        """Set up automatic config saving when values change."""
        # Save config when variables change (with debouncing)
        self._config_save_timer = None
        
        def schedule_save(*args):
            """Schedule config save (debounced)."""
            if self._config_save_timer:
                self.after_cancel(self._config_save_timer)
            self._config_save_timer = self.after(1000, self._save_config)  # Save after 1 second of no changes
        
        # Bind to variable changes (except PAT which is never saved)
        self.folder_path_var.trace_add('write', schedule_save)
        self.username_var.trace_add('write', schedule_save)
        self.repo_name_var.trace_add('write', schedule_save)
        self.visibility_var.trace_add('write', schedule_save)
        self.description_var.trace_add('write', schedule_save)
        self.commit_message_var.trace_add('write', schedule_save)

