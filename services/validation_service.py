"""
Validation service for GitHub Repository Creator.

Provides input validation functions for folder paths, repository names, and tokens.
"""

import os
import re
from pathlib import Path


def validate_folder_path(path: str) -> tuple[bool, str]:
    """
    Validate that a folder path exists and is accessible.
    
    Args:
        path: Path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if path is valid, False otherwise
        - error_message: Empty string if valid, error description if invalid
    """
    if not path:
        return False, "Folder path cannot be empty"
    
    if not isinstance(path, str):
        return False, "Folder path must be a string"
    
    try:
        path_obj = Path(path)
        
        # Check if path exists
        if not path_obj.exists():
            return False, f"Folder does not exist: {path}"
        
        # Check if it's a directory
        if not path_obj.is_dir():
            return False, f"Path is not a directory: {path}"
        
        # Check if directory is readable
        if not os.access(path, os.R_OK):
            return False, f"Folder is not readable: {path}"
        
        # Check if it's already a Git repository (warning, not error)
        git_dir = path_obj / '.git'
        if git_dir.exists() and git_dir.is_dir():
            return True, "Warning: Folder already contains a Git repository"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating folder path: {str(e)}"


def validate_repository_name(name: str) -> tuple[bool, str]:
    """
    Validate GitHub repository name format.
    
    GitHub repository names must:
    - Be 1-100 characters long
    - Contain only alphanumeric characters, hyphens, underscores, and periods
    - Not start or end with a period
    - Not contain consecutive periods
    - Not be a reserved name (basic check)
    
    Args:
        name: Repository name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Repository name cannot be empty"
    
    if not isinstance(name, str):
        return False, "Repository name must be a string"
    
    # Check length
    if len(name) < 1:
        return False, "Repository name must be at least 1 character"
    
    if len(name) > 100:
        return False, "Repository name must be 100 characters or less"
    
    # Check for valid characters (alphanumeric, hyphens, underscores, periods)
    if not re.match(r'^[a-zA-Z0-9._-]+$', name):
        return False, "Repository name can only contain alphanumeric characters, hyphens, underscores, and periods"
    
    # Check for leading/trailing periods
    if name.startswith('.') or name.endswith('.'):
        return False, "Repository name cannot start or end with a period"
    
    # Check for consecutive periods
    if '..' in name:
        return False, "Repository name cannot contain consecutive periods"
    
    # Basic reserved name check (common ones)
    reserved_names = ['.', '..', '.git']
    if name.lower() in reserved_names:
        return False, f"Repository name '{name}' is reserved"
    
    return True, ""


def validate_token(token: str) -> tuple[bool, str]:
    """
    Validate GitHub Personal Access Token format.
    
    GitHub tokens can be:
    - Classic tokens: Start with 'ghp_'
    - Fine-grained tokens: Start with 'github_pat_'
    
    Args:
        token: Token to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not token:
        return False, "Token cannot be empty"
    
    if not isinstance(token, str):
        return False, "Token must be a string"
    
    # Check minimum length (GitHub tokens are typically 40+ characters)
    if len(token) < 20:
        return False, "Token appears too short (GitHub tokens are typically 40+ characters)"
    
    # Check for valid prefixes
    if token.startswith('ghp_'):
        # Classic token format: ghp_ followed by alphanumeric characters
        if len(token) < 40:
            return False, "Classic token appears too short"
        if not re.match(r'^ghp_[a-zA-Z0-9]{36,}$', token):
            return False, "Invalid classic token format"
        return True, ""
    
    elif token.startswith('github_pat_'):
        # Fine-grained token format: github_pat_ followed by alphanumeric characters
        if len(token) < 50:
            return False, "Fine-grained token appears too short"
        if not re.match(r'^github_pat_[a-zA-Z0-9_]{40,}$', token):
            return False, "Invalid fine-grained token format"
        return True, ""
    
    else:
        return False, "Token must start with 'ghp_' (classic) or 'github_pat_' (fine-grained)"

