# GitHub Repository Creator

A GUI application for creating GitHub repositories from local Windows folders.

## Description

This application allows you to:
- Select a local folder
- Create a new GitHub repository
- Initialize Git in the folder
- Automatically handle empty folders (creates `.gitkeep` files to preserve folder structure)
- Push all files and subfolders to GitHub
- Track progress in real-time with detailed status updates
- Handle errors gracefully with user-friendly messages

## Requirements

- Python 3.9+
- Git installed and accessible via command line
- GitHub account with Personal Access Token

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Usage

1. **Launch the application:**
   ```bash
   python main.py
   ```

2. **Select a local folder:**
   - Click the "Browse" button
   - Navigate to and select the folder you want to migrate to GitHub

3. **Enter GitHub credentials:**
   - Enter your GitHub username
   - Enter your Personal Access Token (recommended) or password
   - For token creation, see: [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

4. **Configure repository:**
   - Enter a repository name (alphanumeric, hyphens, underscores, or periods)
   - Choose visibility: Private or Public
   - Optionally add a description

5. **Set commit message:**
   - Enter an initial commit message (default: "Initial commit: add all files and subfolders")

6. **Create and push:**
   - Click "Create Repository & Push"
   - Monitor progress in the status log
   - Wait for completion confirmation

7. **Access your repository:**
   - Once complete, the repository URL will be displayed
   - Click the link to open your repository in a browser

## Common Errors

- **"Git not found"**: Install Git and ensure it's in your system PATH
- **"Invalid token"**: Check that your token starts with `ghp_` (classic tokens) or `github_pat_` (fine-grained tokens)
- **"Repository already exists"**: Choose a different repository name
- **"Folder already contains a Git repository"**: The selected folder already has a `.git` directory. Choose a different folder or remove the existing `.git` folder
- **"Token appears too short"**: GitHub tokens are typically 40+ characters. Verify you copied the complete token

## Development

See `implementation_checklist.md` for development progress and `specification.md` for detailed requirements.

