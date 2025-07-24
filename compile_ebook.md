# eBook Compilation Instructions

## Prerequisites

1. **Install Pandoc**: Download and install Pandoc from https://pandoc.org/installing.html
2. **Verify Installation**: Open a terminal and run `pandoc --version` to confirm it's installed

## Compilation Commands

Once your script finishes generating all the markdown files in the `output/` directory, use these commands to compile your eBook:

### Generate EPUB (Recommended for eReaders)
```bash
pandoc output/*.md -o "The_Quantum_Thief.epub" --toc --metadata title="The Quantum Thief" --metadata creator="Dr. Evelyn Reed" --metadata language="en"
```

### Generate PDF (For Print/Desktop Reading)
```bash
pandoc output/*.md -o "The_Quantum_Thief.pdf" --toc --metadata title="The Quantum Thief" --metadata creator="Dr. Evelyn Reed" --pdf-engine=xelatex
```

### Generate HTML (For Web Reading)
```bash
pandoc output/*.md -o "The_Quantum_Thief.html" --toc --metadata title="The Quantum Thief" --metadata creator="Dr. Evelyn Reed" --standalone --css=style.css
```

### Generate DOCX (For Editing in Word)
```bash
pandoc output/*.md -o "The_Quantum_Thief.docx" --toc --metadata title="The Quantum Thief" --metadata creator="Dr. Evelyn Reed"
```

## Command Explanation

- `output/*.md` - Processes all markdown files in the output directory in alphabetical order
- `--toc` - Generates a table of contents
- `--metadata title="..."` - Sets the book title in the metadata
- `--metadata creator="..."` - Sets the author name in the metadata
- `--metadata language="en"` - Sets the language (useful for EPUB)
- `--standalone` - Creates a complete HTML document (for HTML output)
- `--pdf-engine=xelatex` - Uses XeLaTeX for better PDF generation (requires LaTeX installation)

## Troubleshooting

### If PDF generation fails:
1. Install a LaTeX distribution:
   - **Windows**: MiKTeX (https://miktex.org/)
   - **macOS**: MacTeX (https://www.tug.org/mactex/)
   - **Linux**: `sudo apt-get install texlive-xetex` (Ubuntu/Debian)

### If you want to customize the appearance:
1. Create a CSS file for HTML output
2. Use custom LaTeX templates for PDF output
3. Modify the markdown files before compilation

## Quick Start (After Script Completes)

1. Open terminal in your project directory
2. Run: `pandoc output/*.md -o "The_Quantum_Thief.epub" --toc --metadata title="The Quantum Thief" --metadata creator="Dr. Evelyn Reed"`
3. Your eBook will be ready as `The_Quantum_Thief.epub`!