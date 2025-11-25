# Help Elements and Configuration Persistence Features

## Overview

This document describes the help/info elements and configuration persistence features implemented in the GitHub Repository Creator application.

## Help Elements

### Purpose
Each input field in the application has a help button (?) next to its label that provides users with:
- Expected input format
- Examples of valid input
- Additional relevant information

### Implementation
- **Help Buttons:** Small "?" buttons next to each input field label
- **Help Dialogs:** Modal dialogs that appear when help buttons are clicked
- **Content:** Each dialog contains formatted text with examples and format requirements

### Input Fields with Help
1. **Source Folder Path**
   - Explains folder selection
   - Example: `C:\Users\YourName\Documents\MyProject`
   - Notes about empty folder handling

2. **GitHub Username**
   - Format explanation
   - Example: `octocat`
   - Clarification that it's the username, not email

3. **Personal Access Token**
   - Token format examples (classic and fine-grained)
   - Instructions for creating a token
   - Security note that token is not saved

4. **Repository Name**
   - Naming rules and restrictions
   - Examples: `my-awesome-project`, `python_utils`
   - Character limits and allowed characters

5. **Repository Visibility**
   - Explanation of Private vs Public
   - Default recommendation
   - Note about changing later

6. **Repository Description**
   - Optional field explanation
   - Example descriptions
   - Usage notes

7. **Initial Commit Message**
   - Purpose explanation
   - Example messages
   - Default value information

## Configuration Persistence

### Purpose
User inputs are automatically saved to allow prefilling on next application startup, improving user experience.

### Security
- **⚠️ CRITICAL:** Personal Access Token (PAT) is NEVER saved
- PAT must be re-entered each time the application starts
- Only non-sensitive inputs are persisted

### Implementation

#### Configuration File
- **File Name:** `app_config.json`
- **Location:** Application root directory
- **Git Status:** Excluded from repository (in `.gitignore`)

#### Saved Fields
- `folder_path`: Selected source folder path
- `username`: GitHub username
- `repo_name`: Repository name
- `visibility`: Repository visibility (private/public)
- `description`: Repository description
- `commit_message`: Initial commit message

#### Excluded Fields
- `token`: Personal Access Token (security requirement)
- `pat`: Alternative PAT key (security requirement)

### Auto-Save Behavior
- Configuration is saved automatically when values change (debounced by 1 second)
- Configuration is saved when:
  - User types in any field
  - User selects a folder via browse button
  - User changes visibility selection
  - Application exits

### Load Behavior
- Configuration is loaded on application startup
- Fields are prefilled with saved values
- If no saved configuration exists, fields use default values
- PAT field is always empty on startup (never loaded)

## Technical Details

### Config Utility (`utils/config.py`)
```python
def load_config() -> Dict[str, Any]:
    """Load user configuration from file."""
    # Returns empty dict if file doesn't exist

def save_config(config: Dict[str, Any]) -> bool:
    """Save user configuration to file (excluding PAT)."""
    # Automatically filters out 'token' and 'pat' keys

def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific configuration value."""

def set_config_value(key: str, value: Any) -> bool:
    """Set a specific configuration value (fails for 'token'/'pat')."""
```

### Main Window Integration
```python
class MainWindow(customtkinter.CTk):
    def __init__(self):
        # ... initialization ...
        self._create_widgets()
        self._load_config()  # Prefill fields
        self._setup_config_autosave()  # Enable auto-save
    
    def _load_config(self):
        """Load saved configuration and prefill fields."""
        # Loads config and sets StringVar values
    
    def _save_config(self):
        """Save current field values (excluding PAT)."""
        # Collects current values and saves
    
    def _setup_config_autosave(self):
        """Set up automatic config saving when values change."""
        # Binds to variable changes with debouncing
```

## Testing

A test script is available at `test_steps/test_help_and_config.py` that verifies:
1. Config utility exists and functions correctly
2. PAT is never saved to config file
3. Help methods exist in main window
4. Config file is in `.gitignore`
5. Config save/load works correctly

## User Experience Benefits

1. **Help Elements:**
   - Reduces user confusion
   - Provides immediate guidance
   - Shows examples for each field
   - Explains format requirements

2. **Configuration Persistence:**
   - Saves time on repeated use
   - Remembers user preferences
   - Maintains security (PAT not saved)
   - Seamless user experience

## Security Considerations

- PAT is never persisted to disk
- Config file is excluded from git repository
- No sensitive data in configuration
- Users must re-enter PAT each session
- Config file is plain JSON (not encrypted) but contains no secrets

