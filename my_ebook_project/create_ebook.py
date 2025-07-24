#!/usr/bin/env python3
"""
eBook Creator Script
A Python script to generate eBooks from markdown content using configuration settings.
"""

import json
import os
import sys
from pathlib import Path
import markdown
from datetime import datetime

class EBookCreator:
    def __init__(self, config_file="config.json"):
        """Initialize the eBook creator with configuration."""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file {self.config_file} not found!")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def load_outline(self):
        """Load the book outline from markdown file."""
        outline_file = self.config.get('outline_file', 'outline.md')
        try:
            with open(outline_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Outline file {outline_file} not found!")
            return ""
    
    def create_html_ebook(self):
        """Create an HTML version of the eBook."""
        outline_content = self.load_outline()
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['toc', 'tables', 'fenced_code'])
        html_content = md.convert(outline_content)
        
        # Create HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.get('title', 'My eBook')}</title>
    <meta name="author" content="{self.config.get('author', 'Unknown Author')}">
    <style>
        body {{
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2em;
        }}
        h1 {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            font-style: italic;
        }}
        .title-page {{
            text-align: center;
            margin-bottom: 50px;
            page-break-after: always;
        }}
        .title {{
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        .author {{
            font-size: 1.5em;
            color: #7f8c8d;
        }}
        .date {{
            color: #95a5a6;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1 class="title">{self.config.get('title', 'My eBook')}</h1>
        <p class="author">by {self.config.get('author', 'Unknown Author')}</p>
        <p class="date">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    
    {html_content}
</body>
</html>
        """
        
        # Write HTML file
        output_file = f"{self.config.get('title', 'my_ebook').replace(' ', '_').lower()}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"HTML eBook created: {output_file}")
        return output_file
    
    def create_ebook(self):
        """Main method to create the eBook."""
        print(f"Creating eBook: {self.config.get('title', 'My eBook')}")
        print(f"Author: {self.config.get('author', 'Unknown Author')}")
        print("-" * 50)
        
        # Create HTML version
        html_file = self.create_html_ebook()
        
        print(f"\nEBook creation completed!")
        print(f"Output file: {html_file}")
        
        # Optional: Convert to PDF if dependencies are available
        if self.config.get('create_pdf', False):
            self.create_pdf_from_html(html_file)
    
    def create_pdf_from_html(self, html_file):
        """Convert HTML to PDF (requires additional dependencies)."""
        try:
            import pdfkit
            pdf_file = html_file.replace('.html', '.pdf')
            pdfkit.from_file(html_file, pdf_file)
            print(f"PDF version created: {pdf_file}")
        except ImportError:
            print("PDF creation requires 'pdfkit' library. Install with: pip install pdfkit")
        except Exception as e:
            print(f"Error creating PDF: {e}")

def main():
    """Main function to run the eBook creator."""
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "config.json"
    
    creator = EBookCreator(config_file)
    creator.create_ebook()

if __name__ == "__main__":
    main()