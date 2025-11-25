"""
Configuration management for GitHub Repository Creator.

Handles saving and loading user preferences (excluding sensitive data like PAT).
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


CONFIG_FILE = 'app_config.json'


def load_config() -> Dict[str, Any]:
    """
    Load user configuration from file.
    
    Returns:
        Dictionary with user preferences (empty dict if file doesn't exist)
    """
    if not os.path.isfile(CONFIG_FILE):
        return {}
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, IOError) as e:
        # If file is corrupted, return empty config
        return {}


def save_config(config: Dict[str, Any]) -> bool:
    """
    Save user configuration to file.
    
    Args:
        config: Dictionary with user preferences (PAT will be excluded)
        
    Returns:
        True if successful, False otherwise
    """
    # Remove PAT from config before saving (security requirement)
    safe_config = {k: v for k, v in config.items() if k != 'token' and k != 'pat'}
    
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(safe_config, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get a specific configuration value.
    
    Args:
        key: Configuration key
        default: Default value if key doesn't exist
        
    Returns:
        Configuration value or default
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: Any) -> bool:
    """
    Set a specific configuration value and save.
    
    Args:
        key: Configuration key
        value: Value to set (will be excluded if key is 'token' or 'pat')
        
    Returns:
        True if successful, False otherwise
    """
    config = load_config()
    # Don't save PAT
    if key in ['token', 'pat']:
        return False
    
    config[key] = value
    return save_config(config)

