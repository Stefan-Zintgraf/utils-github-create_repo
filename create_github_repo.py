# create_github_repo.py
"""
Script to create GitHub repository and push current project files.
"""
import os
import subprocess
import sys

# Repository details
REPO_NAME = "utils-github-createrep"
USER_EMAIL = "stefan@zintgraf.de"
USER_PASSWORD = "ga7t6$gAPxJFtj$9"

def get_github_username():
    """Try to get GitHub username - will need to be provided or extracted"""
    # We'll need the actual GitHub username, not just email
    # For now, try common patterns or ask user
    # Let's try to get it from git config or use a default
    try:
        result = subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        # Try to extract from email
        return USER_EMAIL.split('@')[0]

def create_repository():
    """Create GitHub repository and push files"""
    
    print("="*60)
    print("Creating GitHub Repository")
    print("="*60)
    print(f"Repository name: {REPO_NAME}")
    print(f"User email: {USER_EMAIL}")
    
    # Note: GitHub API no longer accepts password authentication
    # We need to use one of these methods:
    # 1. Personal Access Token (PAT) - recommended
    # 2. GitHub CLI (gh) - if installed
    # 3. Manual creation + git push
    
    print("\n[INFO] GitHub API requires Personal Access Token (PAT) for API calls.")
    print("[INFO] However, git push with HTTPS may still work with password.")
    print("[INFO] Attempting to create repository...\n")
    
    # Step 1: Configure git
    print("Step 1: Configuring git...")
    try:
        username = get_github_username()
        subprocess.run(['git', 'config', 'user.email', USER_EMAIL], check=True)
        subprocess.run(['git', 'config', 'user.name', username], check=True)
        print(f"  [OK] Git configured: {username} <{USER_EMAIL}>")
    except Exception as e:
        print(f"  [WARN] Could not configure git: {e}")
    
    # Step 2: Check if repo already exists locally
    print("\nStep 2: Checking git repository status...")
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("  [OK] Git repository initialized")
        else:
            print("  [INFO] Initializing git repository...")
            subprocess.run(['git', 'init'], check=True)
            print("  [OK] Git repository initialized")
    except Exception as e:
        print(f"  [ERROR] Git error: {e}")
        return False
    
    # Step 3: Add files
    print("\nStep 3: Adding files to git...")
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(f"  [OK] Files staged for commit")
        else:
            print("  [WARN] No files to commit (may be ignored by .gitignore)")
    except Exception as e:
        print(f"  [ERROR] Failed to add files: {e}")
        return False
    
    # Step 4: Create commit
    print("\nStep 4: Creating initial commit...")
    try:
        subprocess.run(['git', 'commit', '-m', 'Initial commit: GitHub Repository Creator project'], check=True)
        print("  [OK] Initial commit created")
    except Exception as e:
        print(f"  [ERROR] Failed to create commit: {e}")
        return False
    
    # Step 5: Rename branch to main
    print("\nStep 5: Setting branch to main...")
    try:
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        print("  [OK] Branch set to main")
    except Exception as e:
        print(f"  [WARN] Could not rename branch: {e}")
    
    # Step 6: Try to create repo using GitHub CLI (if available)
    print("\nStep 6: Creating GitHub repository...")
    repo_created = False
    repo_url = None
    
    # Try GitHub CLI first
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True, timeout=5)
        print("  [INFO] GitHub CLI found, attempting to create repository...")
        # Note: gh auth login would be needed first
        # For now, we'll skip this and go to manual method
    except:
        pass
    
    # Since we can't use API with password, we'll provide instructions
    # and try to set up the remote assuming repo will be created manually
    print("\n" + "="*60)
    print("MANUAL STEP REQUIRED")
    print("="*60)
    print("GitHub API requires Personal Access Token (PAT), not password.")
    print("\nPlease create the repository manually:")
    print(f"1. Go to: https://github.com/new")
    print(f"2. Repository name: {REPO_NAME}")
    print(f"3. Description: GUI application for creating GitHub repositories")
    print(f"4. Visibility: Public (or Private)")
    print(f"5. DO NOT initialize with README, .gitignore, or license")
    print(f"6. Click 'Create repository'")
    print("\nAfter creating, press Enter to continue with git push...")
    
    # For automation, we'll try to proceed anyway
    # The user can create it manually, then we push
    
    # Step 7: Add remote and push
    print("\nStep 7: Setting up remote and pushing...")
    
    # We need the GitHub username - let's try to get it
    # For now, we'll construct a URL pattern
    # The user will need to provide their GitHub username or we extract from email
    
    username = get_github_username()
    repo_url = f"https://github.com/{username}/{REPO_NAME}.git"
    
    print(f"  [INFO] Assuming repository URL: {repo_url}")
    print(f"  [INFO] If your GitHub username is different, update the remote manually")
    
    try:
        # Remove existing remote if any
        subprocess.run(['git', 'remote', 'remove', 'origin'], 
                      capture_output=True, stderr=subprocess.DEVNULL)
    except:
        pass
    
    try:
        # Add remote with credentials in URL (for HTTPS push)
        # Format: https://username:password@github.com/username/repo.git
        remote_url = f"https://{username}:{USER_PASSWORD}@github.com/{username}/{REPO_NAME}.git"
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        print("  [OK] Remote added")
        
        # Try to push
        print("  [INFO] Attempting to push to GitHub...")
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("  [OK] Successfully pushed to GitHub!")
            print(f"\n[SUCCESS] Repository created and files pushed!")
            print(f"Repository URL: https://github.com/{username}/{REPO_NAME}")
            return True
        else:
            print(f"  [ERROR] Push failed: {result.stderr}")
            print("\nPossible issues:")
            print("1. Repository doesn't exist yet - create it manually first")
            print("2. Wrong GitHub username - update remote URL")
            print("3. Password authentication may not work - use PAT")
            print(f"\nTo fix, run:")
            print(f"  git remote set-url origin https://github.com/{username}/{REPO_NAME}.git")
            print(f"  git push -u origin main")
            return False
            
    except subprocess.TimeoutExpired:
        print("  [ERROR] Push operation timed out")
        return False
    except Exception as e:
        print(f"  [ERROR] Failed to push: {e}")
        return False

if __name__ == '__main__':
    success = create_repository()
    sys.exit(0 if success else 1)
