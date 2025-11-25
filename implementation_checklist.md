# Implementation Checklist

This checklist provides a step-by-step approach for implementing the GitHub Repository Creator application. Each step is designed to be testable through automation and generates log files for error detection and fixing.

**Note:** For detailed test scripts, verification code, and implementation hints, see `implementation_hints.md`.

## Automatic Checkbox Updates

**All checkboxes in this checklist are automatically updated when test scripts complete successfully.**

The `update_checklist.py` script is called automatically by test scripts to:
- Mark prerequisites as complete when verified
- Mark steps as complete when tests pass
- Update the progress summary in real-time

**Manual Update (if needed):**
```bash
# Update prerequisites
python update_checklist.py prerequisites

# Update a specific step
python update_checklist.py <phase> <step>
# Example: python update_checklist.py 1 1.1
```

**Note:** Test scripts automatically call this update function, so manual updates should rarely be needed.

## ⚠️ CRITICAL: Step Completion Requirements

**Every step completion MUST include these three mandatory actions:**

1. **Archive Files:** Store all files, folders, and related artifacts in a subfolder within `step_archive/` named with the pattern `p{phase}_s{step}`
2. **Create Test Script:** Create and store test script in `test_steps/test_step_X_Y.py`
3. **⚠️ MANDATORY GIT COMMIT/PUSH:** Execute `git add . && git commit -m "Step X.Y: [description]" && git push origin main`

**The git commit/push step (step 3) is MANDATORY and must NOT be skipped. Automation agents must complete this before proceeding to the next step.**

**Every checklist step must also include the creation of a runnable `test_step_X_Y.py` script that verifies that step's functionality, exercises `update_checklist.py`, and confirms the step's checkbox when executed. Writing that script is part of the step's implementation work. All test scripts must be stored in the `test_steps/` subfolder.**

**Examples:**
- Phase 1, Step 1.1 → `step_archive/p1_s1.1/` and `test_steps/test_step_1_1.py`
- Phase 2, Step 2.3 → `step_archive/p2_s2.3/` and `test_steps/test_step_2_3.py`
- Phase 3, Step 3.2 → `step_archive/p3_s3.2/` and `test_steps/test_step_3_2.py`

**What to store:**
- All source code files created/modified in that step
- Test files and test results
- Log files generated during testing
- Any configuration files
- Documentation updates

**Storage Process:**

**Automated Process (Preferred):**
1. Complete the step implementation (automation agent, e.g., Codex, will orchestrate all required edits and script generation)
2. Create test script `test_steps/test_step_X_Y.py` (automation agent creates this)
3. Run the test script and verify success (automation agent runs each `test_steps/test_step_X_Y.py`)
4. Re-run every `test_steps/test_step_X_Y.py` script introduced so far, including previous steps, to ensure no regressions are introduced; adjust older scripts as needed to reflect intentional interfaces and requirements
5. Copy all step-related files to the appropriate subfolder (e.g., `step_archive/p3_s3.2/`) and gather logs (automation agent automates this archival)
6. Checkboxes are automatically updated by test scripts (see `update_checklist.py`)
7. **⚠️ CRITICAL: Update and push to git repository (MANDATORY - DO NOT SKIP):** (automation agent MUST execute `git add`, commit, and push once validation passes)
   - Add files: `git add .` (step archive folder `step_archive/` and test steps folder `test_steps/` are automatically excluded via `.gitignore`)
   - Commit: `git commit -m "Step X.Y: [Step description]"`
   - Push: `git push origin main`
   - **Note:** This step is MANDATORY and must be completed before moving to the next step. The automation agent must NOT proceed to the next step without completing this git workflow.
8. Verify the checkbox is checked in the progress summary below

**Manual Process (if automation not available):**
1. Complete step implementation
2. Create test script `test_steps/test_step_X_Y.py` (see `implementation_hints.md` for template)
3. Run test script and verify success: `python test_steps/test_step_X_Y.py`
4. Check success log: `logs/step_X_Y_success.log`
5. Copy all step-related files to subfolder `step_archive/p{phase}_s{step}/` (e.g., `step_archive/p3_s3.2/`)
6. Maintain directory structure within the subfolder
7. Update checklist: `python update_checklist.py {phase} {step}`
8. Commit and push: `git add . && git commit -m "Step X.Y: [description]" && git push origin main`

**Automation Note:** An automation agent (e.g., Codex) is responsible for running the entire workflow described above—test execution, regression checks, artifact archiving, checklist updates, and **MANDATORY git commits/pushes**—without requiring any direct input from you unless a specific decision is needed (e.g., choosing between conflicting implementations). The agent should not stop mid-step or request confirmation unless a course of action cannot be determined automatically. Unless explicitly instructed to halt before a phase, the automation agent completes the full lifecycle for every step so nothing is left half-finished.

**⚠️ CRITICAL REMINDER FOR AUTOMATION AGENTS:** Step 7 (git commit and push) is MANDATORY and must be executed after every step. The automation agent must NOT skip this step or proceed to the next step without completing the git workflow. Each step must result in a separate git commit with the format: `git commit -m "Step X.Y: [Step description]"` followed by `git push origin main`.

**Important:** The `step_archive/` and `test_steps/` folders are in `.gitignore` and must never be committed to the repository. They are for local step storage and testing only.

## Implementation Progress Summary

### Prerequisites
- [ ] Python 3.9+ installed
- [ ] Git installed and accessible via command line
- [ ] GitHub account with Personal Access Token
- [ ] Test folder structure for validation

### Phase 1: Project Setup
- [ ] Step 1.1: Create Project Structure
- [x] Step 1.2: Create Requirements File
- [x] Step 1.3: Create Logging Directory and Utility

### Phase 2: Core Services
- [x] Step 2.1: Create Validation Service
- [x] Step 2.2: Create Git Service - Basic Structure
- [x] Step 2.3: Implement create_gitkeep_files Method
- [x] Step 2.4: Implement Git Operations Methods
- [x] Step 2.5: Create GitHub Service

### Phase 3: User Interface
- [x] Step 3.1: Create Main Window Structure
- [x] Step 3.2: Implement UI Event Handlers
- [x] Step 3.3: Implement Background Threading

### Phase 4: Integration
- [ ] Step 4.1: Create Main Entry Point
- [x] Step 4.2: End-to-End Integration Test

### Phase 5: Error Handling & Polish
- [x] Step 5.1: Implement Comprehensive Error Handling
- [ ] Step 5.2: Create .gitignore File

---

## Phase 1: Project Setup

### Step 1.1: Create Project Structure
**Objective:** Set up the basic project directory structure

**Files to Create:**
- `main.py`
- `requirements.txt`
- `README.md`
- `.gitignore`
- `ui/__init__.py`
- `services/__init__.py`
- `utils/__init__.py`

**Test:** Create and run `test_steps/test_step_1_1.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p1_s1.1/` subfolder after successful testing
2. Store test script in `test_steps/test_step_1_1.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 1.1: Create Project Structure" && git push origin main`

---

### Step 1.2: Create Requirements File
**Objective:** Define all Python dependencies

**Files to Create/Modify:**
- `requirements.txt` with: customtkinter>=5.2.0, PyGithub>=2.1.1, GitPython>=3.1.40, requests>=2.31.0

**Test:** Create and run `test_steps/test_step_1_2.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p1_s1.2/` subfolder after successful testing
2. Store test script in `test_steps/test_step_1_2.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 1.2: Create Requirements File" && git push origin main`

---

### Step 1.3: Create Logging Directory and Utility
**Objective:** Set up logging infrastructure

**Files to Create:**
- `utils/logger.py`
- `logs/` directory (auto-created)

**Test:** Create and run `test_steps/test_step_1_3.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p1_s1.3/` subfolder after successful testing
2. Store test script in `test_steps/test_step_1_3.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 1.3: Create Logging Directory and Utility" && git push origin main`

---

## Phase 2: Core Services

### Step 2.1: Create Validation Service
**Objective:** Implement input validation functions

**Files to Create:**
- `services/validation_service.py`

**Required Functions:**
- `validate_folder_path(path: str) -> tuple[bool, str]`
- `validate_repository_name(name: str) -> tuple[bool, str]`
- `validate_token(token: str) -> tuple[bool, str]`

**Test:** Create and run `test_steps/test_step_2_1.py` - See `implementation_hints.md` for test script template

**⚠️ SECURITY REQUIREMENT:** 
- Test files must NOT contain token strings (real or fake) in the source code
- Fake test tokens must be loaded from `test_tokens.json` (which is in `.gitignore`)
- This prevents GitGuardian and similar security scanners from flagging committed files

**After Completion:** 
1. Store all files in `step_archive/p2_s2.1/` subfolder after successful testing
2. Store test script in `test_steps/test_step_2_1.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 2.1: Create Validation Service" && git push origin main`

---

### Step 2.2: Create Git Service - Basic Structure
**Objective:** Create GitService class with method stubs

**Files to Create:**
- `services/git_service.py`

**Required Methods:**
- `__init__(repo_path: str)`
- `initialize_repo() -> bool`
- `create_gitkeep_files() -> int`
- `stage_all_files() -> tuple[int, int]`
- `commit(message: str) -> bool`
- `add_remote(url: str) -> bool`
- `rename_branch(branch_name: str) -> bool`
- `push(branch: str, remote: str) -> bool`

**Test:** Create and run `test_steps/test_step_2_2.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p2_s2.2/` subfolder after successful testing
2. Store test script in `test_steps/test_step_2_2.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 2.2: Create Git Service - Basic Structure" && git push origin main`

---

### Step 2.3: Implement create_gitkeep_files Method
**Objective:** Implement logic to create .gitkeep files in empty folders

**Files to Modify:**
- `services/git_service.py`

**Functionality:**
- Recursively scan all directories
- Identify empty folders (containing no files, only subdirectories)
- Note: Folders containing only `.gitkeep` files are considered empty
- Hidden files (starting with `.`) are treated as regular files
- Create `.gitkeep` file in each empty folder
- Return count of files created

**Test:** Create and run `test_steps/test_step_2_3.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p2_s2.3/` subfolder after successful testing
2. Store test script in `test_steps/test_step_2_3.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 2.3: Implement create_gitkeep_files Method" && git push origin main`

---

### Step 2.4: Implement Git Operations Methods
**Objective:** Implement all Git command execution methods

**Files to Modify:**
- `services/git_service.py`

**Methods to Implement:**
- `initialize_repo()` - Execute `git init`
- `stage_all_files()` - Execute `git add .` and return file count
- `commit(message)` - Execute `git commit -m`
- `add_remote(url)` - Execute `git remote add origin`
- `rename_branch(branch)` - Execute `git branch -M`
- `push(branch, remote)` - Execute `git push -u`

**Test:** Create and run `test_steps/test_step_2_4.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p2_s2.4/` subfolder after successful testing
2. Store test script in `test_steps/test_step_2_4.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 2.4: Implement Git Operations Methods" && git push origin main`

---

### Step 2.5: Create GitHub Service
**Objective:** Implement GitHub API integration

**Files to Create:**
- `services/github_service.py`

**Required Methods:**
- `__init__(token: str)`
- `validate_token(token: str) -> bool`
- `create_repository(name: str, private: bool, description: str) -> str`
- `check_repository_exists(name: str) -> bool`

**Test:** Create and run `test_steps/test_step_2_5.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p2_s2.5/` subfolder after successful testing
2. Store test script in `test_steps/test_step_2_5.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 2.5: Create GitHub Service" && git push origin main`

---

## Phase 3: User Interface

### Step 3.1: Create Main Window Structure
**Objective:** Create basic CustomTkinter window with all UI components

**Files to Create:**
- `ui/main_window.py`

**Required Components:**
- Window initialization with minimum size (600x400) and default size (800x600)
- **Scrollable content area** using CTkScrollableFrame to ensure all elements are accessible
- All input fields (folder path, username, token, repo name, etc.)
- **Help/info buttons (?) next to each input field label** showing expected input format and examples
- All buttons (browse, create, clear, exit)
- Progress bar
- Status text area
- **Scrollbars must appear automatically when content exceeds window height**
- **Configuration management:** Load saved inputs on startup, save inputs automatically (excluding PAT)

**⚠️ UI REQUIREMENT:** The window must be scrollable to work on smaller screens. All UI elements must be accessible via scrolling.

**⚠️ UI REQUIREMENT - Help Elements:**
- Each input field must have a help button (?) next to its label
- Help buttons open modal dialogs with:
  - Expected input format
  - Examples of valid input
  - Additional relevant information

**⚠️ UI REQUIREMENT - Input Persistence:**
- All user inputs (except PAT) must be saved to `app_config.json` (excluded from git)
- Fields must be prefilled from saved config on startup
- Config must be saved automatically when values change (debounced)
- PAT must NEVER be saved to configuration file

**Test:** Create and run `test_steps/test_step_3_1.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p3_s3.1/` subfolder after successful testing
2. Store test script in `test_steps/test_step_3_1.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 3.1: Create Main Window Structure" && git push origin main`

---

### Step 3.2: Implement UI Event Handlers
**Objective:** Connect UI components to functionality

**Files to Modify:**
- `ui/main_window.py`

**Required Handlers:**
- `on_browse_clicked()` - Open folder dialog
- `on_create_clicked()` - Start repository creation process
- `on_clear_clicked()` - Reset all fields
- `_create_help_button()` - Create help/info button next to input fields
- `_show_help_dialog()` - Show modal help dialog with information
- `_load_config()` - Load saved configuration and prefill fields (excluding PAT)
- `_save_config()` - Save current field values to config file (excluding PAT)
- `_setup_config_autosave()` - Set up automatic config saving when values change
- `update_status(message, error)` - Update status log
- `update_progress(value)` - Update progress bar

**⚠️ REQUIREMENT:** Help buttons must be implemented for all input fields with relevant examples and format information.

**⚠️ REQUIREMENT:** Configuration persistence must be implemented to save/load user inputs (excluding PAT).

**Test:** Create and run `test_steps/test_step_3_2.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p3_s3.2/` subfolder after successful testing
2. Store test script in `test_steps/test_step_3_2.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 3.2: Implement UI Event Handlers" && git push origin main`

---

### Step 3.3: Implement Background Threading
**Objective:** Run Git/GitHub operations in background thread

**Files to Modify:**
- `ui/main_window.py`

**Functionality:**
- `on_create_clicked()` should start background thread
- UI should remain responsive during operations
- Status updates should be thread-safe

**Test:** Create and run `test_steps/test_step_3_3.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p3_s3.3/` subfolder after successful testing
2. Store test script in `test_steps/test_step_3_3.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 3.3: Implement Background Threading" && git push origin main`

---

## Phase 4: Integration

### Step 4.1: Create Main Entry Point
**Objective:** Create main.py that launches the application

**Files to Create/Modify:**
- `main.py`

**Functionality:**
- Import and create MainWindow
- Start application event loop
- Handle application exit

**Test:** Create and run `test_steps/test_step_4_1.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p4_s4.1/` subfolder after successful testing
2. Store test script in `test_steps/test_step_4_1.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 4.1: Create Main Entry Point" && git push origin main`

---

### Step 4.2: End-to-End Integration Test
**Objective:** Test complete workflow

**Test Scenario:**
1. Create test folder structure
2. Initialize Git
3. Create .gitkeep files
4. Stage files
5. Commit
6. Create GitHub repository (mock)
7. Add remote
8. Push (mock)

**Test:** Create and run `test_steps/test_step_4_2.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p4_s4.2/` subfolder after successful testing
2. Store test script in `test_steps/test_step_4_2.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 4.2: End-to-End Integration Test" && git push origin main`

---

## Phase 5: Error Handling & Polish

### Step 5.1: Implement Comprehensive Error Handling
**Objective:** Add error handling to all methods

**Files to Modify:**
- All service files
- UI files

**Test Criteria:**
- All methods handle exceptions gracefully
- User-friendly error messages displayed
- Errors logged to log files
- Application doesn't crash on errors

**Test:** Create and run `test_steps/test_step_5_1.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p5_s5.1/` subfolder after successful testing
2. Store test script in `test_steps/test_step_5_1.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 5.1: Implement Comprehensive Error Handling" && git push origin main`

---

### Step 5.2: Create .gitignore File
**Objective:** Add proper .gitignore for Python project

**Files to Create/Modify:**
- `.gitignore`

**Content Should Include:**
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments
- IDE files
- Log files
- Test directories

**Test:** Create and run `test_steps/test_step_5_2.py` - See `implementation_hints.md` for test script template

**After Completion:** 
1. Store all files in `step_archive/p5_s5.2/` subfolder after successful testing
2. Store test script in `test_steps/test_step_5_2.py`
3. **⚠️ MANDATORY:** Commit and push to git: `git add . && git commit -m "Step 5.2: Create .gitignore File" && git push origin main`

---

## Test Execution

### Run Individual Tests
```bash
python test_steps/test_step_X_Y.py
```

### Run All Tests
```bash
python run_all_tests.py
```

### Check Logs
- Success logs: `logs/step_X_Y_success.log`
- Error logs: `logs/step_X_Y_errors.log`
- Summary: `logs/test_summary.log`

### GUI Testing Notes

**Important:** For GUI-related steps (Phase 3), automated tests verify:
- Component structure and existence
- Method callability
- Basic functionality

**After automated tests pass, manual GUI testing is required:**
- Visual appearance and layout
- User interaction flow
- Real-time UI responsiveness
- Error message display

See `implementation_hints.md` for detailed GUI testing strategy and manual test checklists.

For detailed test scripts and verification code, see `implementation_hints.md`.
