# test_prerequisites.py
import os
import sys
import subprocess

def test_prerequisites():
    """Test all prerequisites for the GitHub Repository Creator application"""
    
    errors = []
    warnings = []
    results = {}
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Test 1: Python version
    print("Testing Python version...")
    try:
        result = subprocess.run(
            [sys.executable, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        version_str = result.stdout.strip()
        print(f"  Found: {version_str}")
        
        # Extract version number
        version_parts = version_str.split()[1].split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major > 3 or (major == 3 and minor >= 9):
            results['python'] = True
            print(f"  [OK] Python {major}.{minor} meets requirement (>= 3.9)")
        else:
            results['python'] = False
            errors.append(f"Python version {major}.{minor} does not meet requirement (>= 3.9)")
            print(f"  [FAIL] Python {major}.{minor} does not meet requirement")
    except Exception as e:
        results['python'] = False
        errors.append(f"Could not check Python version: {str(e)}")
        print(f"  [FAIL] Error checking Python: {str(e)}")
    
    # Test 2: Git installation
    print("\nTesting Git installation...")
    try:
        result = subprocess.run(
            ['git', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_str = result.stdout.strip()
            print(f"  Found: {version_str}")
            results['git'] = True
            print("  [OK] Git is installed and accessible")
        else:
            results['git'] = False
            errors.append("Git command returned non-zero exit code")
            print("  [FAIL] Git command failed")
    except FileNotFoundError:
        results['git'] = False
        errors.append("Git is not installed or not in PATH")
        print("  [FAIL] Git not found in PATH")
    except Exception as e:
        results['git'] = False
        errors.append(f"Error checking Git: {str(e)}")
        print(f"  [FAIL] Error checking Git: {str(e)}")
    
    # Test 3: GitHub account and token (cannot verify automatically)
    print("\nTesting GitHub account...")
    print("  [WARN] GitHub account and Personal Access Token cannot be verified automatically")
    print("  [WARN] Please ensure you have:")
    print("     - A GitHub account")
    print("     - A Personal Access Token (PAT) with repo permissions")
    warnings.append("GitHub account and token require manual verification")
    results['github'] = None  # Cannot verify automatically
    
    # Test 4: Test folder structure
    print("\nTesting folder structure...")
    test_folder = "test_folder_structure"
    try:
        if not os.path.exists(test_folder):
            os.makedirs(test_folder)
            # Create a sample structure
            os.makedirs(os.path.join(test_folder, "empty_dir"))
            with open(os.path.join(test_folder, "test_file.txt"), 'w') as f:
                f.write("Test content")
            print(f"  [OK] Created test folder structure: {test_folder}/")
            results['test_folder'] = True
        else:
            print(f"  [OK] Test folder already exists: {test_folder}/")
            results['test_folder'] = True
    except Exception as e:
        results['test_folder'] = False
        errors.append(f"Could not create test folder: {str(e)}")
        print(f"  [FAIL] Error creating test folder: {str(e)}")
    
    # Summary
    print("\n" + "="*60)
    print("PREREQUISITES TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    warnings_count = len(warnings)
    
    print(f"\nPassed: {passed}")
    print(f"Failed: {failed}")
    print(f"Warnings: {warnings_count}")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  [FAIL] {error}")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  [WARN] {warning}")
    
    # Write results to log file
    if errors:
        with open('logs/prerequisites_errors.log', 'w') as f:
            f.write("PREREQUISITES TEST ERRORS\n")
            f.write("="*60 + "\n\n")
            for error in errors:
                f.write(f"[FAIL] {error}\n")
            f.write("\n" + "="*60 + "\n")
            f.write(f"Total Errors: {len(errors)}\n")
        print(f"\n[FAIL] Prerequisites test FAILED - See logs/prerequisites_errors.log")
        return False
    else:
        with open('logs/prerequisites_success.log', 'w') as f:
            f.write("PREREQUISITES TEST SUCCESS\n")
            f.write("="*60 + "\n\n")
            f.write("All prerequisites verified:\n\n")
            f.write(f"[OK] Python: {sys.version}\n")
            f.write(f"[OK] Git: Installed and accessible\n")
            f.write(f"[WARN] GitHub: Requires manual verification\n")
            f.write(f"[OK] Test folder: Created successfully\n")
            f.write("\n" + "="*60 + "\n")
            f.write("Status: READY TO PROCEED\n")
        print(f"\n[OK] Prerequisites test PASSED - See logs/prerequisites_success.log")
        
        # Automatically update checkboxes in checklist
        try:
            from update_checklist import update_prerequisites
            update_prerequisites()
            print("Checkboxes updated in implementation_checklist.md")
        except Exception as e:
            print(f"Warning: Could not update checkboxes: {str(e)}")
        
        return True

if __name__ == '__main__':
    success = test_prerequisites()
    sys.exit(0 if success else 1)

