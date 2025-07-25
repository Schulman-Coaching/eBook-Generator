# eBook Generator

An AI-powered Python package that automatically generates complete eBooks using Google's Gemini AI, based on detailed outlines.

## 🚀 Quick Start

### Installation

#### Option 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/Schulman-Coaching/eBook-Generator.git@v1.0.0
```

#### Option 2: Local Development Installation
```bash
git clone https://github.com/Schulman-Coaching/eBook-Generator.git
cd eBook-Generator
pip install -e .
```

#### Option 3: Install Dependencies Only
```bash
pip install google-generativeai
```

### Basic Usage

#### Command Line Interface
```bash
# Generate an eBook using the default config.json
ebook-gen

# Or use the full command name
ebook-generator
```

#### Python API
```python
from ebook_generator import EbookGenerator

# Initialize and generate
generator = EbookGenerator('config.json')
success = generator.generate_ebook(output_dir='output')

if success:
    print("eBook generated successfully!")
```

## 📁 Project Structure

```
eBook-Generator/
├── ebook_generator/         # Main package
│   ├── __init__.py         # Package initialization
│   ├── generator.py        # Main EbookGenerator class
│   ├── config.py           # Configuration management
│   ├── content.py          # AI content generation
│   └── utils.py            # Utility functions
├── examples/               # Usage examples
│   ├── basic_usage.py      # Basic usage example
│   ├── sample_config.json  # Sample configuration
│   └── sample_outline.md   # Sample outline
├── setup.py               # Package installation
├── requirements.txt       # Dependencies
├── config.json           # Your book configuration
├── outline.md            # Your book outline
└── README.md            # This file
```

## ⚙️ Configuration

Create a `config.json` file with your book details:

```json
{
    "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE",
    "book_title": "Your Book Title",
    "subtitle": "Your Book Subtitle",
    "author_name": "Your Name",
    "genre": "Your Genre",
    "target_audience": "Your Target Audience",
    "tone": "Your Desired Tone",
    "word_count_per_chapter": 2500,
    "outline_file": "outline.md"
}
```

### Configuration Fields

- `gemini_api_key`: Your Google AI Studio API key
- `book_title`: Main title of your book
- `subtitle`: Book subtitle
- `author_name`: Author name
- `genre`: Book genre (affects writing style)
- `target_audience`: Intended readers
- `tone`: Writing tone and style
- `word_count_per_chapter`: Target words per chapter
- `outline_file`: Path to your outline file

## 📖 Creating Your Outline

Structure your `outline.md` file with:
- Chapter titles as H2 headers (`## Chapter 1: Title`)
- Detailed descriptions for each chapter
- Character information, plot points, or key concepts
- The more detail you provide, the better the AI-generated content

Example:
```markdown
# Your Book Title

## Introduction: Setting the Stage
Detailed description of what this introduction should cover...

## Chapter 1: The Beginning
Detailed description of the first chapter content...

## Chapter 2: The Development
Detailed description of the second chapter content...
```

## 🤖 How It Works

1. **Parses** your outline to extract chapter titles
2. **Generates** front matter (title page, copyright, dedication)
3. **Creates** each chapter with context from previous chapters
4. **Maintains** story continuity through chapter summaries
5. **Produces** back matter (about the author)
6. **Saves** all content as numbered markdown files

## 📚 Compilation Options

Use Pandoc to create various formats:

```bash
# EPUB (recommended)
pandoc output/*.md -o "book.epub" --toc --metadata title="Your Title" --metadata creator="Your Name"

# PDF
pandoc output/*.md -o "book.pdf" --toc --pdf-engine=xelatex

# HTML
pandoc output/*.md -o "book.html" --toc --standalone

# DOCX
pandoc output/*.md -o "book.docx" --toc
```

## 🔧 Requirements

- Python 3.7+
- `google-generativeai` library
- Pandoc (for final compilation)
- Google AI Studio API key

## 💡 Usage Examples

### Basic Generation
```python
from ebook_generator import EbookGenerator

generator = EbookGenerator()
generator.generate_ebook()
```

### Custom Configuration
```python
from ebook_generator import EbookGenerator

generator = EbookGenerator('my_custom_config.json')
success = generator.generate_ebook(output_dir='my_output')
```

### Preview Before Generation
```python
from ebook_generator import EbookGenerator

generator = EbookGenerator()

# Preview book info
book_info = generator.get_book_info()
print(f"Generating: {book_info['title']} by {book_info['author']}")

# Preview chapters
chapters = generator.preview_chapters()
print(f"Found {len(chapters)} chapters to generate")

# Generate
generator.generate_ebook()
```

## 🚨 Important Notes

- The package includes rate limiting (2-second delays between API calls)
- Failed generations are retried up to 3 times
- Each chapter maintains context from previous chapters
- Generated files are numbered for proper compilation order

## 🔄 Version Management

This package uses semantic versioning. The current stable version is tagged as `v1.0.0`.

### Using Specific Versions
```bash
# Install specific version
pip install git+https://github.com/Schulman-Coaching/eBook-Generator.git@v1.0.0

# Install latest development version
pip install git+https://github.com/Schulman-Coaching/eBook-Generator.git@main
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Customize and use as needed for your eBook projects.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Schulman-Coaching/eBook-Generator/issues)
- **Documentation**: This README and inline code documentation
- **Examples**: Check the `examples/` directory

---

**Happy Writing! 📝✨**