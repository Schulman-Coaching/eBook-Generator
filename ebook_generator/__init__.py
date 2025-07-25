"""
eBook Generator - AI-powered eBook generation using Google's Gemini AI

A Python package for automatically generating complete eBooks from detailed outlines
using Google's Gemini AI API.
"""

__version__ = "1.0.0"
__author__ = "Elie Schulman"
__email__ = "elie@schulmancoaching.com"

from .generator import EbookGenerator
from .config import load_config, setup_gemini
from .content import ContentGenerator
from .utils import parse_outline, create_output_directory

__all__ = [
    'EbookGenerator',
    'load_config',
    'setup_gemini',
    'ContentGenerator',
    'parse_outline',
    'create_output_directory'
]