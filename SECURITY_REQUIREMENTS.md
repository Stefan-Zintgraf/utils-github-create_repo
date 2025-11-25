# Security Requirements for Token Handling

## Critical Rule: No Tokens in Repository Files

**⚠️ MANDATORY:** No tokens (real or fake) shall be stored in any file that is committed to the repository.

### Why This Matters

- **GitGuardian and similar security scanners** will flag any token-like strings, even if they're fake
- Committing token strings (even fake ones) can trigger security alerts
- This creates unnecessary noise and potential security review overhead

### Requirements

1. **Test Files:**
   - Test scripts must NOT contain token strings in source code
   - Fake test tokens must be loaded from external files that are in `.gitignore`
   - Use `test_tokens.json` (or similar) for storing fake test tokens

2. **Test Token File:**
   - File name: `test_tokens.json`
   - Must be listed in `.gitignore`
   - Contains fake tokens for testing purposes only
   - Never committed to the repository

3. **Fallback Behavior:**
   - If `test_tokens.json` doesn't exist, tests should generate tokens dynamically
   - Generated tokens should be clearly fake (e.g., using "TEST" repeated)
   - Never hardcode token strings in source files

### Implementation Pattern

```python
# ✅ CORRECT: Load from external file
try:
    with open('test_tokens.json', 'r') as f:
        test_tokens = json.load(f)
    fake_token = test_tokens['fake_classic_token']
except FileNotFoundError:
    # Generate dynamically if file doesn't exist
    fake_token = 'ghp_' + 'TEST' * 9  # Clearly fake, generated at runtime

# ❌ WRONG: Hardcoded in source file
fake_token = 'ghp_1234567890abcdef1234567890abcdef12345678'  # DON'T DO THIS - This will be flagged by GitGuardian!
```

### Files That Must Never Contain Tokens

- Any `.py` file in the repository
- Any `.md` file in the repository
- Any configuration file that is committed
- Test files (`test_steps/*.py`)

### Files That May Contain Tokens (but are in .gitignore)

- `test_tokens.json` - Fake tokens for testing
- `github_token.txt` - Real tokens (if used, must be in .gitignore)
- Any file explicitly listed in `.gitignore`

### Verification

Before committing, verify:
- [ ] No token strings in any `.py` files
- [ ] No token strings in any `.md` files
- [ ] `test_tokens.json` is in `.gitignore`
- [ ] All test files load tokens from external files or generate them dynamically

