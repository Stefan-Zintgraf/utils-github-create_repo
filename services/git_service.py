"""
Git service for GitHub Repository Creator.

Handles all Git operations including initialization, staging, committing, and pushing.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional

try:
    from git import Repo
    GITPYTHON_AVAILABLE = True
except ImportError:
    GITPYTHON_AVAILABLE = False


class GitService:
    """Service for executing Git operations."""
    
    def __init__(self, repo_path: str):
        """
        Initialize GitService with repository path.
        
        Args:
            repo_path: Path to the repository directory
        """
        self.repo_path = Path(repo_path).resolve()
        self.repo: Optional[Repo] = None
        
        # Try to initialize GitPython repo if available
        if GITPYTHON_AVAILABLE:
            try:
                if (self.repo_path / '.git').exists():
                    self.repo = Repo(self.repo_path)
            except Exception:
                # GitPython not available or repo not initialized yet
                pass
    
    def initialize_repo(self) -> bool:
        """
        Initialize a Git repository in the specified path.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if GITPYTHON_AVAILABLE and self.repo is None:
                # Use GitPython if available
                self.repo = Repo.init(self.repo_path)
                return True
            else:
                # Use subprocess as fallback
                result = subprocess.run(
                    ['git', 'init'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    # Update repo reference if GitPython is available
                    if GITPYTHON_AVAILABLE:
                        try:
                            self.repo = Repo(self.repo_path)
                        except Exception:
                            pass
                    return True
                return False
        except Exception:
            return False
    
    def create_gitkeep_files(self) -> int:
        """
        Create .gitkeep files in all empty folders.
        
        Recursively scans all directories and creates .gitkeep files
        in folders that contain no files and no subdirectories (leaf directories).
        Note: Folders containing only .gitkeep files are considered empty.
        Hidden files (starting with '.') are treated as regular files.
        
        Returns:
            Number of .gitkeep files created
        """
        count = 0
        gitkeep_name = '.gitkeep'
        
        def is_empty_leaf_folder(folder_path: Path) -> bool:
            """
            Check if a folder is an empty leaf directory (no files, no subdirectories).
            Folders containing only .gitkeep files are considered empty.
            """
            try:
                items = list(folder_path.iterdir())
                
                has_files = False
                has_subdirs = False
                
                for item in items:
                    # Skip .git directory
                    if item.name == '.git' and item.is_dir():
                        continue
                    
                    # If it's a file
                    if item.is_file():
                        if item.name != gitkeep_name:
                            has_files = True
                            break
                    # If it's a directory
                    elif item.is_dir():
                        has_subdirs = True
                
                # Empty if no files (except .gitkeep) and no subdirectories
                return not has_files and not has_subdirs
            except (PermissionError, OSError):
                # Can't read directory, skip it
                return False
        
        # Recursively walk through all directories
        for root, dirs, files in os.walk(self.repo_path):
            root_path = Path(root)
            
            # Skip .git directory
            if '.git' in root_path.parts:
                continue
            
            # Check if this directory is an empty leaf folder
            if is_empty_leaf_folder(root_path):
                gitkeep_path = root_path / gitkeep_name
                
                # Only create if it doesn't already exist
                if not gitkeep_path.exists():
                    try:
                        gitkeep_path.touch()
                        count += 1
                    except (PermissionError, OSError):
                        # Can't create file, skip
                        pass
        
        return count
    
    def stage_all_files(self) -> tuple[int, int]:
        """
        Stage all files in the repository.
        
        Returns:
            Tuple of (file_count, total_size_in_bytes)
        """
        try:
            # Stage all files
            if GITPYTHON_AVAILABLE and self.repo:
                # Use GitPython
                self.repo.git.add('.')
                # Count files
                file_count = 0
                total_size = 0
                for item in self.repo_path.rglob('*'):
                    if item.is_file() and '.git' not in item.parts:
                        file_count += 1
                        total_size += item.stat().st_size
                return file_count, total_size
            else:
                # Use subprocess
                result = subprocess.run(
                    ['git', 'add', '.'],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    # Count files manually
                    file_count = 0
                    total_size = 0
                    for root, dirs, files in os.walk(self.repo_path):
                        # Skip .git directory
                        if '.git' in root:
                            continue
                        for file in files:
                            file_path = Path(root) / file
                            if file_path.is_file():
                                file_count += 1
                                try:
                                    total_size += file_path.stat().st_size
                                except OSError:
                                    pass
                    return file_count, total_size
                return 0, 0
        except Exception:
            return 0, 0
    
    def commit(self, message: str) -> bool:
        """
        Create a commit with the given message.
        
        Args:
            message: Commit message
            
        Returns:
            True if successful, False otherwise
        """
        if not message or not message.strip():
            return False
        
        try:
            if GITPYTHON_AVAILABLE and self.repo:
                # Use GitPython
                self.repo.index.commit(message)
                return True
            else:
                # Use subprocess
                result = subprocess.run(
                    ['git', 'commit', '-m', message],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                return result.returncode == 0
        except Exception:
            return False
    
    def add_remote(self, url: str) -> bool:
        """
        Add a remote repository URL.
        
        Args:
            url: Remote repository URL
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if GITPYTHON_AVAILABLE and self.repo:
                # Use GitPython - remove existing remote if it exists
                try:
                    self.repo.delete_remote('origin')
                except Exception:
                    pass
                self.repo.create_remote('origin', url)
                return True
            else:
                # Use subprocess - remove existing remote if it exists
                subprocess.run(
                    ['git', 'remote', 'remove', 'origin'],
                    cwd=self.repo_path,
                    capture_output=True,
                    check=False
                )
                # Add new remote
                result = subprocess.run(
                    ['git', 'remote', 'add', 'origin', url],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                return result.returncode == 0
        except Exception:
            return False
    
    def rename_branch(self, branch_name: str) -> bool:
        """
        Rename the current branch.
        
        Args:
            branch_name: New branch name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if GITPYTHON_AVAILABLE and self.repo:
                # Use GitPython
                try:
                    self.repo.git.branch('-M', branch_name)
                    return True
                except Exception:
                    # Branch might already be named correctly
                    return True
            else:
                # Use subprocess
                result = subprocess.run(
                    ['git', 'branch', '-M', branch_name],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                # Return True even if branch is already named correctly
                return result.returncode == 0 or 'already exists' in result.stderr.lower()
        except Exception:
            return False
    
    def push(self, branch: str, remote: str = "origin") -> bool:
        """
        Push commits to remote repository.
        
        Args:
            branch: Branch name to push
            remote: Remote name (default: "origin")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if GITPYTHON_AVAILABLE and self.repo:
                # Use GitPython
                origin = self.repo.remote(remote)
                origin.push(branch, set_upstream=True)
                return True
            else:
                # Use subprocess
                result = subprocess.run(
                    ['git', 'push', '-u', remote, branch],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    check=False
                )
                return result.returncode == 0
        except Exception:
            return False

