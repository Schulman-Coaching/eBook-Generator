"""
Configuration management for the eBook Generator.
"""

import json
import google.generativeai as genai


def load_config(config_path='config.json'):
    """Loads configuration from a JSON file.
    
    Args:
        config_path (str): Path to the configuration JSON file
        
    Returns:
        dict: Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    print("Loading configuration...")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def setup_gemini(api_key):
    """Configures the Gemini API client.
    
    Args:
        api_key (str): Google AI Studio API key
        
    Returns:
        genai.GenerativeModel: Configured Gemini model instance
    """
    print("Initializing Gemini API...")
    genai.configure(api_key=api_key)
    # Using a model optimized for longer, creative text generation
    return genai.GenerativeModel('gemini-2.5-pro')


def validate_config(config):
    """Validates the configuration dictionary.
    
    Args:
        config (dict): Configuration dictionary to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    required_fields = [
        'gemini_api_key', 'book_title', 'author_name', 
        'genre', 'target_audience', 'tone', 'outline_file'
    ]
    
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required configuration field: {field}")
    
    if not config.get("gemini_api_key") or config["gemini_api_key"] == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        raise ValueError("Gemini API key is missing or not set properly")
    
    return True