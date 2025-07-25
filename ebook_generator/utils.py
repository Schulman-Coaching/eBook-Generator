"""
Utility functions for the eBook Generator.
"""

import os
import re


def parse_outline(filepath):
    """Parses the outline file to extract chapter titles.
    
    Args:
        filepath (str): Path to the outline markdown file
        
    Returns:
        list: List of chapter titles, or None if file not found
    """
    print(f"Parsing outline file: {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Assumes chapters are H2 headings (## Chapter Title)
        chapters = re.findall(r'^##\s*(.*)', content, re.MULTILINE)
        if not chapters:
            print("Warning: No chapters found. Ensure they are formatted as '## Chapter Title'.")
        return chapters
    except FileNotFoundError:
        print(f"Error: Outline file not found at '{filepath}'.")
        return None


def create_output_directory(path='output'):
    """Creates the output directory if it doesn't exist.
    
    Args:
        path (str): Path to the output directory
        
    Returns:
        str: The created directory path
    """
    print(f"Ensuring output directory '{path}' exists...")
    os.makedirs(path, exist_ok=True)
    return path


def sanitize_filename(filename):
    """Sanitizes a filename by removing or replacing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename safe for filesystem use
    """
    # Remove or replace characters that are invalid in filenames
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing whitespace and dots
    filename = filename.strip(' .')
    # Limit length to reasonable size
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def format_chapter_filename(chapter_number, title, prefix="chapter"):
    """Formats a chapter filename with proper numbering and sanitization.
    
    Args:
        chapter_number (int): Chapter number
        title (str): Chapter title
        prefix (str): Filename prefix (default: "chapter")
        
    Returns:
        str: Formatted filename
    """
    sanitized_title = sanitize_filename(title.lower().replace(' ', '_'))
    return f"{chapter_number + 2:02d}_{prefix}_{chapter_number}_{sanitized_title}.md"


def count_words(text):
    """Counts words in a text string.
    
    Args:
        text (str): Text to count words in
        
    Returns:
        int: Number of words
    """
    if not text:
        return 0
    return len(text.split())


def estimate_reading_time(word_count, words_per_minute=200):
    """Estimates reading time based on word count.
    
    Args:
        word_count (int): Number of words
        words_per_minute (int): Average reading speed (default: 200)
        
    Returns:
        str: Formatted reading time estimate
    """
    if word_count <= 0:
        return "0 minutes"
    
    minutes = word_count / words_per_minute
    
    if minutes < 1:
        return "Less than 1 minute"
    elif minutes < 60:
        return f"{int(minutes)} minutes"
    else:
        hours = int(minutes // 60)
        remaining_minutes = int(minutes % 60)
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''} {remaining_minutes} minutes"