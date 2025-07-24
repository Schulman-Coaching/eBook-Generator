import os
import zipfile
import tempfile
import shutil
from pathlib import Path

def fix_epub_encoding(epub_path):
    """Fix encoding issues in an EPUB file by extracting, fixing, and recompiling."""
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        extract_dir = os.path.join(temp_dir, 'epub_content')
        
        # Extract EPUB (it's just a ZIP file)
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find and fix text files
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.endswith(('.html', '.xhtml', '.xml', '.opf', '.ncx')):
                    file_path = os.path.join(root, file)
                    try:
                        # Read with latin1 and write as UTF-8
                        with open(file_path, 'r', encoding='latin1') as f:
                            content = f.read()
                        
                        # Fix common encoding issues
                        content = content.replace('�', '—')  # Replace � with em dash
                        content = content.replace('â€™', "'")  # Fix apostrophe
                        content = content.replace('â€œ', '"')  # Fix opening quote
                        content = content.replace('â€', '"')   # Fix closing quote
                        
                        # Write back as UTF-8
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                            
                    except Exception as e:
                        print(f"Could not fix {file_path}: {e}")
        
        # Create new EPUB
        fixed_epub_path = epub_path.replace('.epub', '_fixed.epub')
        
        # Recreate ZIP/EPUB
        with zipfile.ZipFile(fixed_epub_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, extract_dir)
                    zip_ref.write(file_path, arc_path)
        
        print(f"Fixed EPUB saved as: {fixed_epub_path}")
        return fixed_epub_path

if __name__ == "__main__":
    epub_file = "Prompting_Humans_Learning_How_to_Ask_For_What_They_Want.epub"
    if os.path.exists(epub_file):
        fix_epub_encoding(epub_file)
    else:
        print(f"EPUB file {epub_file} not found!")