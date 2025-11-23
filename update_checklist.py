# update_checklist.py
"""
Script to automatically update checkboxes in implementation_checklist.md
after completing steps. This should be called by test scripts after successful completion.
"""
import os
import re

CHECKLIST_FILE = 'implementation_checklist.md'

def update_checkbox(item_name, checked=True):
    """
    Update a checkbox in the checklist file.
    
    Args:
        item_name: Name of the item to check (e.g., "Python 3.9+ installed", "Step 1.1: Create Project Structure")
        checked: True to check, False to uncheck
    """
    if not os.path.isfile(CHECKLIST_FILE):
        print(f"Error: {CHECKLIST_FILE} not found")
        return False
    
    with open(CHECKLIST_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match checkboxes: - [ ] or - [x] followed by the item name
    # Handle both exact matches and partial matches (for step names)
    pattern = r'(- \[)([ x])(\] ' + re.escape(item_name) + r')'
    
    # Try exact match first
    match = re.search(pattern, content, re.IGNORECASE)
    
    if not match:
        # Try partial match (item name might be part of a longer line)
        pattern = r'(- \[)([ x])(\] .*' + re.escape(item_name) + r')'
        match = re.search(pattern, content, re.IGNORECASE)
    
    if match:
        checkbox_char = 'x' if checked else ' '
        replacement = match.group(1) + checkbox_char + match.group(3)
        content = content[:match.start()] + replacement + content[match.end():]
        
        with open(CHECKLIST_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated checkbox: {item_name} -> {'[x]' if checked else '[ ]'}")
        return True
    else:
        print(f"Warning: Could not find checkbox for: {item_name}")
        return False

def update_prerequisites():
    """Update all prerequisite checkboxes based on test results"""
    # Check if prerequisites test passed
    if os.path.isfile('logs/prerequisites_success.log'):
        update_checkbox("Python 3.9+ installed", True)
        update_checkbox("Git installed and accessible via command line", True)
        update_checkbox("Test folder structure for validation", True)
        # GitHub account cannot be automatically verified, so leave it unchecked
        print("Prerequisites checkboxes updated (except GitHub - requires manual verification)")
        return True
    return False

def update_step(phase, step, checked=True):
    """
    Update a step checkbox.
    
    Args:
        phase: Phase number (e.g., 1, 2, 3)
        step: Step number (e.g., 1.1, 2.3)
        checked: True to check, False to uncheck
    """
    step_name = f"Step {step}:"
    return update_checkbox(step_name, checked)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'prerequisites':
            update_prerequisites()
        elif len(sys.argv) >= 3:
            # Format: python update_checklist.py phase step [checked]
            phase = sys.argv[1]
            step = sys.argv[2]
            checked = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else True
            update_step(phase, step, checked)
        else:
            item_name = ' '.join(sys.argv[1:])
            update_checkbox(item_name, True)
    else:
        print("Usage:")
        print("  python update_checklist.py prerequisites")
        print("  python update_checklist.py <phase> <step>")
        print("  python update_checklist.py '<item name>'")

