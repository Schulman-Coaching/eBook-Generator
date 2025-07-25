#!/usr/bin/env python3
"""
Basic usage example for the eBook Generator package.

This example demonstrates how to use the eBook Generator programmatically
to generate an eBook from a configuration file and outline.
"""

import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ebook_generator import EbookGenerator


def main():
    """Demonstrate basic usage of the eBook Generator."""
    
    print("eBook Generator - Basic Usage Example")
    print("=" * 40)
    
    # Initialize the generator
    # By default, it looks for 'config.json' in the current directory
    generator = EbookGenerator()
    
    # Preview the book information (optional)
    print("\n1. Loading configuration...")
    if generator.load_configuration():
        book_info = generator.get_book_info()
        if book_info:
            print(f"   Title: {book_info['title']}")
            print(f"   Author: {book_info['author']}")
            print(f"   Genre: {book_info['genre']}")
            print(f"   Target Audience: {book_info['target_audience']}")
    
    # Preview chapters (optional)
    print("\n2. Previewing chapters...")
    chapters = generator.preview_chapters()
    if chapters:
        print(f"   Found {len(chapters)} chapters:")
        for i, chapter in enumerate(chapters[:5], 1):  # Show first 5
            print(f"   {i}. {chapter}")
        if len(chapters) > 5:
            print(f"   ... and {len(chapters) - 5} more chapters")
    
    # Generate the eBook
    print("\n3. Generating eBook...")
    success = generator.generate_ebook(output_dir='output')
    
    if success:
        print("\n✅ eBook generation completed successfully!")
        print("\nNext steps:")
        print("1. Review the generated files in the 'output' directory")
        print("2. Use Pandoc to compile into your desired format:")
        print("   pandoc output/*.md -o my_book.epub --toc")
    else:
        print("\n❌ eBook generation failed. Check the error messages above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())