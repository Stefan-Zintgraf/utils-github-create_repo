"""
GitHub service for GitHub Repository Creator.

Handles GitHub API operations including repository creation and token validation.
"""

from typing import Optional

try:
    from github import Github
    from github.GithubException import GithubException
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False
    Github = None
    GithubException = Exception


class GitHubService:
    """Service for executing GitHub API operations."""
    
    def __init__(self, token: str):
        """
        Initialize GitHubService with authentication token.
        
        Args:
            token: GitHub Personal Access Token
        """
        self.token = token
        self.github: Optional[Github] = None
        
        if PYGITHUB_AVAILABLE:
            try:
                self.github = Github(token)
            except Exception:
                pass
    
    def validate_token(self, token: Optional[str] = None) -> bool:
        """
        Validate GitHub Personal Access Token.
        
        Args:
            token: Token to validate (uses instance token if None)
            
        Returns:
            True if token is valid, False otherwise
        """
        test_token = token or self.token
        if not test_token:
            return False
        
        if not PYGITHUB_AVAILABLE:
            return False
        
        try:
            github = Github(test_token)
            # Try to get authenticated user
            user = github.get_user()
            # If we can get the user, token is valid
            _ = user.login
            return True
        except Exception:
            return False
    
    def create_repository(
        self,
        name: str,
        private: bool = True,
        description: str = ""
    ) -> str:
        """
        Create a new GitHub repository.
        
        Args:
            name: Repository name
            private: Whether repository should be private (default: True)
            description: Repository description (optional)
            
        Returns:
            Repository URL (HTTPS)
            
        Raises:
            Exception: If repository creation fails
        """
        if not PYGITHUB_AVAILABLE or not self.github:
            raise Exception("PyGithub library not available")
        
        try:
            user = self.github.get_user()
            repo = user.create_repo(
                name=name,
                private=private,
                description=description if description else None,
                auto_init=False  # Don't initialize with README
                # Note: gitignore_template and license_template are omitted
                # PyGithub doesn't accept None for these optional parameters
            )
            return repo.clone_url
        except GithubException as e:
            if e.status == 422:
                # Repository might already exist
                raise Exception(f"Repository '{name}' already exists or name is invalid")
            elif e.status == 401:
                raise Exception("Authentication failed. Please check your token.")
            else:
                raise Exception(f"Failed to create repository: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to create repository: {str(e)}")
    
    def check_repository_exists(self, name: str) -> bool:
        """
        Check if a repository with the given name already exists.
        
        Args:
            name: Repository name to check
            
        Returns:
            True if repository exists, False otherwise
        """
        if not PYGITHUB_AVAILABLE or not self.github:
            return False
        
        try:
            user = self.github.get_user()
            try:
                repo = user.get_repo(name)
                return repo is not None
            except GithubException as e:
                if e.status == 404:
                    return False
                # Other errors might mean it exists but we can't access it
                return False
        except Exception:
            return False

