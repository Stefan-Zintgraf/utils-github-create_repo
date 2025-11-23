# New GitHub Repository Setup

## Objective

Migrate a given local Windows folder to a new GitHub repository, ensuring all files and subfolders are included. Create a GUI based application to accomplish this task.

## Source Location

- **Path:** To be provided as user input
- **Platform:** Windows 11
- **Content:** All files and folders recursively

## Github Repository

- **Login-Data:** To be provided as user input
- **Repository-Name:** To be provided as user input

# Example Implementation Steps from a previous manual session

The below text describes general steps to create a new github repository and a concrete example for a specific folder that handles NinjaTrader custom stuff.

## 1. Create New GitHub Repository

1. Sign in to GitHub (https://github.com)
2. Click the "+" icon in the top-right corner
3. Select "New repository"
4. Enter a meaningful repository name
5. Choose visibility (private or public)
6. Do not initialize with README, .gitignore, or license (will be added locally)
7. Click "Create repository"
8. Copy the repository URL (HTTPS or SSH)

## 2. Initialize Git Locally

Open PowerShell on Windows 11 and navigate to the folder:

```
cd "C:\Users\s.zintgraf.ACONTIS\Documents\NinjaTrader 8\bin\Custom"
```

Initialize Git:

```
git init
```

## 3. Add All Files and Subfolders

Add all files and recursive subfolders to staging:

```
git add .
```

This command ensures that all files and subdirectories within the Custom folder are included.

## 4. Commit Files

Create an initial commit with a descriptive message:

```
git commit -m "Initial commit: add all files and subfolders"
```

## 5. Configure Remote Repository

Add the GitHub repository as the remote origin:

```
git remote add origin <repository-URL>
```

Replace `<repository-URL>` with the URL copied from GitHub (either HTTPS or SSH format).

## 6. Push to GitHub

Rename the default branch to `main` and push:

```
git branch -M main
git push -u origin main
```

This uploads all files and subfolders to the GitHub repository.

# Considerations and Best Practices

## File Size and Content

- Ensure that no large binary files or sensitive information (credentials, API keys) are included
- NinjaTrader custom indicators and scripts are typically reasonable in size
- Consider using `.gitignore` if certain file types should be excluded

## Empty Folder Handling

- Git does not track empty directories by default
- The application automatically creates `.gitkeep` files in all empty folders before staging
- This ensures the complete folder structure is preserved in the repository
- The `.gitkeep` file is a standard convention (empty file with `.gitkeep` extension)
- Users can later add actual files to these folders, and the `.gitkeep` can be removed if desired

## Branch Management

- The initial push uses the `main` branch as the primary branch
- Future updates can be pushed with: `git push origin main`

## Subsequent Updates

To update the repository after initial setup:

```
cd "C:\Users\s.zintgraf.ACONTIS\Documents\NinjaTrader 8\bin\Custom"
git add .
git commit -m "Update: description of changes"
git push origin main
```

# Workflow Summary

| Step | Command | Purpose |
|------|---------|---------|
| Navigate | `cd "C:\Users\s.zintgraf.ACONTIS\Documents\NinjaTrader 8\bin\Custom"` | Move to target folder |
| Initialize | `git init` | Create local Git repository |
| Stage All | `git add .` | Add all files and subfolders |
| Commit | `git commit -m "Initial commit..."` | Create first commit |
| Add Remote | `git remote add origin <URL>` | Link to GitHub repository |
| Rename Branch | `git branch -M main` | Set primary branch name |
| Push | `git push -u origin main` | Upload to GitHub |

# Completion

After running the `git push -u origin main` command:

- All files and subfolders from the Custom folder are now on GitHub
- The local repository is linked to the remote GitHub repository
- Future changes can be committed and pushed using standard Git workflow

# References

[1] Git Documentation - Getting Started. https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control

[2] GitHub Documentation - Creating a Repository. https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository

[3] Git - add command documentation. https://git-scm.com/docs/git-add

[4] Git - push command documentation. https://git-scm.com/docs/git-push

# Application Specification

## Technology Stack

### Core Technologies
- **Programming Language:** Python 3.9+
- **GUI Framework:** CustomTkinter 5.x
- **GitHub API:** PyGithub library
- **Git Operations:** GitPython library (with subprocess fallback)
- **Platform:** Windows 11 (primary), cross-platform compatible

### Dependencies
```
customtkinter>=5.2.0
PyGithub>=2.1.1
GitPython>=3.1.40
requests>=2.31.0
```

## Application Architecture

### High-Level Design
- **Type:** Single-window desktop application
- **Architecture:** Event-driven GUI with background task execution
- **Threading:** Background thread for Git/GitHub operations to prevent UI freezing
- **Error Handling:** Comprehensive try-catch blocks with user-friendly error messages

### Component Structure
```
GitHubRepoCreator/
├── main.py                 # Application entry point
├── ui/
│   └── main_window.py      # Main GUI window class
├── services/
│   ├── github_service.py   # GitHub API operations
│   ├── git_service.py      # Git command execution
│   └── validation_service.py # Input validation
├── utils/
│   ├── logger.py           # Logging utility
│   └── config.py           # Configuration management
└── requirements.txt        # Python dependencies
```

## User Interface Design

### Main Window Layout

#### Window Properties
- **Title:** "GitHub Repository Creator"
- **Size:** 800x700 pixels (resizable)
- **Theme:** CustomTkinter dark/light mode (system preference)
- **Icon:** GitHub icon (if available)

#### UI Components (Top to Bottom)

1. **Header Section**
   - Title label: "Create GitHub Repository"
   - Subtitle: "Migrate local folder to GitHub"

2. **Source Folder Section**
   - Label: "Source Folder Path"
   - Entry field: Text input for folder path
   - Browse button: Opens folder selection dialog
   - Validation indicator: Green checkmark or red X

3. **GitHub Authentication Section**
   - Label: "GitHub Authentication"
   - Username field: Text input
   - Token/Password field: Password-masked input
   - Info label: "Use Personal Access Token (recommended)"
   - Link: "How to create a token" (opens browser)

4. **Repository Details Section**
   - Label: "Repository Name"
   - Entry field: Text input (alphanumeric, hyphens, underscores)
   - Label: "Visibility"
   - Radio buttons: "Private" (default) / "Public"
   - Label: "Description" (optional)
   - Text area: Multi-line description input

5. **Commit Message Section**
   - Label: "Initial Commit Message"
   - Entry field: Text input
   - Default value: "Initial commit: add all files and subfolders"

6. **Progress Section**
   - Progress bar: Indeterminate or determinate based on operation
   - Status text area: Scrollable log of operations
   - Auto-scroll: Automatically scrolls to latest message

7. **Action Buttons Section**
   - "Create Repository & Push" button: Primary action (large, prominent)
   - "Clear" button: Reset all fields
   - "Exit" button: Close application

### UI States

#### Initial State
- All fields empty
- Buttons enabled
- Progress bar hidden

#### Processing State
- All input fields disabled
- Action button disabled with "Processing..." text
- Progress bar visible and animated
- Status log showing current operation

#### Success State
- Success message in status log
- Repository URL displayed (clickable link)
- Option to open repository in browser
- Fields remain disabled until reset

#### Error State
- Error message displayed in status log (red text)
- Action button re-enabled
- Input fields remain enabled for correction

## Functional Requirements

### Core Features

#### 1. Folder Selection
- **Browse Dialog:** Native Windows folder picker
- **Path Validation:** 
  - Check if folder exists
  - Check if folder is readable
  - Check if folder is not already a Git repository (with override option)
- **Display:** Show selected path in entry field

#### 2. GitHub Authentication
- **Token Authentication (Primary):**
  - Accept GitHub Personal Access Token
  - Validate token format (starts with `ghp_` for classic tokens)
  - Test token validity with API call
- **Username/Password (Fallback):**
  - Support basic auth (less secure, not recommended)
  - Display warning about security
- **Token Storage:** 
  - Option to save token locally (encrypted)
  - Never store passwords

#### 3. Repository Creation
- **API Call:** Create repository via GitHub API
- **Parameters:**
  - Repository name (validated)
  - Visibility (private/public)
  - Description (optional)
  - Auto-initialize: false (no README, .gitignore, license)
- **Error Handling:**
  - Repository name already exists
  - Invalid repository name format
  - Authentication failure
  - Network errors

#### 4. Git Operations
- **Initialize Repository:**
  - Check if `.git` folder exists
  - If exists, ask user to proceed or abort
  - Execute `git init`
  
- **Handle Empty Folders:**
  - Before staging files, scan all directories recursively
  - Identify all empty folders (folders containing no files)
  - Create a `.gitkeep` file in each empty folder
  - This ensures empty folders are tracked in Git (Git doesn't track empty directories)
  - Log the number of `.gitkeep` files created
  
- **Stage Files:**
  - Execute `git add .`
  - Show count of files staged (including `.gitkeep` files)
  
- **Create Commit:**
  - Execute `git commit -m "<message>"`
  - Validate commit message is not empty
  
- **Configure Remote:**
  - Execute `git remote add origin <repository-url>`
  - Handle case where remote already exists (remove and re-add)
  
- **Rename Branch:**
  - Execute `git branch -M main`
  - Handle case where branch is already `main`
  
- **Push to GitHub:**
  - Execute `git push -u origin main`
  - Handle authentication prompts
  - Show progress for large uploads

#### 5. Progress Tracking
- **Real-time Updates:**
  - Display each operation step
  - Show success/failure for each step
  - Display file count and size information
  - Show count of `.gitkeep` files created for empty folders
  - Show elapsed time

#### 6. Error Handling
- **Validation Errors:**
  - Invalid folder path
  - Invalid repository name
  - Missing authentication
  - Network connectivity issues
  
- **Git Errors:**
  - Git not installed
  - Git command failures
  - Authentication failures
  - Merge conflicts (unlikely for initial push)
  
- **GitHub API Errors:**
  - Rate limiting
  - Authentication failures
  - Repository creation failures
  - Network timeouts

### Advanced Features

#### 1. .gitignore Support
- **Option:** "Create .gitignore file"
- **Templates:** Common .gitignore templates (Python, C#, etc.)
- **Custom:** Allow user to specify custom .gitignore content

#### 2. README Generation
- **Option:** "Create README.md"
- **Template:** Basic README with repository name and description
- **Custom:** Allow user to provide custom README content

#### 3. Repository Settings
- **Advanced Options:**
  - Custom branch name (default: `main`)
  - Custom remote name (default: `origin`)
  - Skip files larger than X MB (warning)
  - Exclude specific file patterns

#### 4. History/Logging
- **Operation Log:** Save operation history to log file
- **Error Log:** Separate error log file
- **View Logs:** Button to open log file location

## Technical Implementation Details

### GitHub Service (`github_service.py`)

```python
class GitHubService:
    def __init__(self, token: str):
        # Initialize PyGithub client
        
    def create_repository(self, name: str, private: bool, description: str) -> str:
        # Create repository and return URL
        
    def validate_token(self, token: str) -> bool:
        # Test token validity
        
    def check_repository_exists(self, name: str) -> bool:
        # Check if repository name is available
```

### Git Service (`git_service.py`)

```python
class GitService:
    def __init__(self, repo_path: str):
        # Initialize GitPython repo or use subprocess
        
    def initialize_repo(self) -> bool:
        # Execute git init
        
    def create_gitkeep_files(self) -> int:
        # Scan all directories recursively
        # Identify empty folders (containing no files, only subdirectories)
        # Create .gitkeep file in each empty folder
        # Return count of .gitkeep files created
        # Note: This must be called before stage_all_files()
        
    def stage_all_files(self) -> tuple[int, int]:
        # Execute git add . and return (file_count, total_size)
        # Note: This includes .gitkeep files created by create_gitkeep_files()
        
    def commit(self, message: str) -> bool:
        # Execute git commit
        
    def add_remote(self, url: str) -> bool:
        # Execute git remote add origin
        
    def rename_branch(self, branch_name: str) -> bool:
        # Execute git branch -M
        
    def push(self, branch: str, remote: str) -> bool:
        # Execute git push with progress tracking
```

### Validation Service (`validation_service.py`)

```python
class ValidationService:
    @staticmethod
    def validate_folder_path(path: str) -> tuple[bool, str]:
        # Validate folder exists and is accessible
        
    @staticmethod
    def validate_repository_name(name: str) -> tuple[bool, str]:
        # Validate GitHub repository name format
        
    @staticmethod
    def validate_token(token: str) -> tuple[bool, str]:
        # Validate token format
```

### Main Window (`main_window.py`)

```python
class MainWindow(customtkinter.CTk):
    def __init__(self):
        # Initialize UI components
        
    def on_browse_clicked(self):
        # Handle folder browse button
        
    def on_create_clicked(self):
        # Handle create repository button
        # Run operations in background thread
        
    def update_status(self, message: str, error: bool = False):
        # Update status log
        
    def update_progress(self, value: int = None):
        # Update progress bar
```

## Security Considerations

### Authentication
- **Token Storage:** 
  - Option to save token in encrypted local storage
  - Use Windows Credential Manager or encrypted config file
  - Never log tokens in status messages
  
### Input Validation
- **Path Validation:** 
  - Prevent directory traversal attacks
  - Validate path is within allowed directories (if applicable)
  
- **Repository Name:** 
  - Sanitize input to prevent injection
  - Follow GitHub naming conventions
  
### Error Messages
- **Information Disclosure:** 
  - Don't expose full error details to users
  - Log detailed errors to file only
  - Show user-friendly messages

## Performance Requirements

### Response Times
- **UI Updates:** < 100ms
- **Folder Validation:** < 500ms
- **Token Validation:** < 2 seconds
- **Repository Creation:** < 5 seconds
- **Git Operations:** Depends on file count and size

### Resource Usage
- **Memory:** < 100MB for typical operations
- **CPU:** Minimal during idle, moderate during Git operations
- **Network:** Efficient use of GitHub API (respect rate limits)

## Testing Requirements

### Unit Tests
- Validation functions
- GitHub service methods
- Git service methods
- Error handling

### Integration Tests
- End-to-end repository creation
- Error scenarios
- Edge cases (empty folder, large files, etc.)

### Manual Testing
- UI responsiveness
- User experience
- Error message clarity
- Progress indication

## Deployment

### Distribution
- **Executable:** PyInstaller to create standalone `.exe` file
- **Installer:** Optional NSIS installer for Windows
- **Requirements:** 
  - Python 3.9+ runtime (if not bundled)
  - Git must be installed on system

### Installation
- **Prerequisites Check:** Verify Git installation on startup
- **Configuration:** Optional config file for default settings
- **Updates:** Manual update mechanism (check for new version)

## Future Enhancements

### Phase 2 Features
- Support for multiple repositories
- Batch processing
- Repository templates
- Custom commit hooks
- Integration with other Git hosts (GitLab, Bitbucket)

### Phase 3 Features
- Command-line interface option
- Configuration profiles
- Scheduled backups
- Repository statistics

## Development Workflow and Git Management

### Step Completion Process

After each implementation step is completed:

1. **Complete Implementation:**
   - Implement the step according to the checklist
   - Run the test script and verify success

2. **Store Step Files:**
   - Copy all step-related files to subfolder `p{phase}_s{step}/` (e.g., `p1_s1.1/`)
   - Maintain directory structure within the subfolder

3. **Update Git Repository:**
   - Add all modified/new project files to git: `git add .`
   - **Important:** Step subfolders (`p*_s*/`) are automatically excluded via `.gitignore` and must never be committed
   - Commit with descriptive message: `git commit -m "Step X.Y: [Step description]"`
   - Push to remote: `git push origin main`

4. **Update Checklist:**
   - Checkboxes are automatically updated by test scripts

### Git Repository Rules

- **Step subfolders excluded:** All `p*_s*/` folders are in `.gitignore` and must never be added to the repository
- **Automatic commits:** Each completed step should result in a git commit and push
- **Commit messages:** Use format "Step X.Y: [description]" for clarity
- **Repository sync:** Keep the remote repository up-to-date after each step

## Development Phases

### Phase 1: Core Functionality (MVP)
1. Basic UI with all input fields
2. Folder selection and validation
3. GitHub repository creation
4. Basic Git operations (init, add, commit, push)
5. Progress indication
6. Basic error handling

### Phase 2: Polish & Enhancement
1. Advanced error handling
2. .gitignore support
3. README generation
4. Token storage
5. Logging system
6. UI improvements

### Phase 3: Advanced Features
1. Advanced repository options
2. Batch operations
3. History/logging UI
4. Settings management
5. Help documentation

## Success Criteria

### Functional
- ✅ Successfully create GitHub repository from local folder
- ✅ Handle all error cases gracefully
- ✅ Provide clear user feedback
- ✅ Complete operation in reasonable time

### User Experience
- ✅ Intuitive interface
- ✅ Clear error messages
- ✅ Progress indication
- ✅ Professional appearance

### Technical
- ✅ Clean, maintainable code
- ✅ Comprehensive error handling
- ✅ Proper logging
- ✅ Cross-platform compatibility (Windows primary)
