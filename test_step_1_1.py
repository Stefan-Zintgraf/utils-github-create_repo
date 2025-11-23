# test_step_1_1.py
import os
import sys

def test_structure():
    errors = []
    
    required_dirs = ['ui', 'services', 'utils']
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        'ui/__init__.py',
        'services/__init__.py',
        'utils/__init__.py'
    ]
    
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            errors.append(f"Directory missing: {dir_name}")
    
    for file_name in required_files:
        if not os.path.isfile(file_name):
            errors.append(f"File missing: {file_name}")
    
    if errors:
        with open('logs/step_1_1_errors.log', 'w') as f:
            f.write('\n'.join(errors))
        return False
    else:
        with open('logs/step_1_1_success.log', 'w') as f:
            f.write("Step 1.1: Project structure created successfully\n\n")
            f.write("Created directories:\n")
            for dir_name in required_dirs:
                f.write(f"  - {dir_name}/\n")
            f.write("\nCreated files:\n")
            for file_name in required_files:
                f.write(f"  - {file_name}\n")
        
        # Automatically update checkbox
        try:
            from update_checklist import update_step
            update_step(1, "1.1", True)
            print("Checkbox updated in checklist")
        except Exception as e:
            print(f"Warning: Could not update checkbox: {str(e)}")
        
        return True

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    success = test_structure()
    if success:
        print("Step 1.1 test PASSED - Project structure created successfully")
    else:
        print("Step 1.1 test FAILED - Check logs/step_1_1_errors.log")
    sys.exit(0 if success else 1)

