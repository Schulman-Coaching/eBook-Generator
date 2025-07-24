# Automated eBook Generator

An AI-powered system that automatically generates complete eBooks using Google's Gemini AI, based on a detailed outline.

## 🚀 Quick Start

1. **Configure your book**: Edit `config.json` with your book details and Gemini API key
2. **Create your outline**: Write detailed chapter descriptions in `outline.md`
3. **Generate content**: Run `python create_ebook.py`
4. **Compile eBook**: Use Pandoc to create your final eBook format

## 📁 Project Structure

```
├── create_ebook.py      # Main generation script
├── config.json          # Book configuration and API key
├── outline.md           # Detailed book outline
├── compile_ebook.md     # Pandoc compilation instructions
├── output/              # Generated content (created after running script)
│   ├── 00_title_page.md
│   ├── 01_copyright.md
│   ├── 02_dedication.md
│   ├── 03_chapter_1.md
│   └── ...
└── README.md           # This file
```

## ⚙️ Configuration

Edit `config.json` to customize your book:

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

## 🤖 How It Works

1. **Parses** your outline to extract chapter titles
2. **Generates** front matter (title page, copyright, dedication)
3. **Creates** each chapter with context from previous chapters
4. **Maintains** story continuity through chapter summaries
5. **Produces** back matter (about the author)
6. **Saves** all content as numbered markdown files

## 📚 Compilation Options

Use Pandoc to create various formats:

- **EPUB**: `pandoc output/*.md -o "book.epub" --toc`
- **PDF**: `pandoc output/*.md -o "book.pdf" --toc --pdf-engine=xelatex`
- **HTML**: `pandoc output/*.md -o "book.html" --toc --standalone`
- **DOCX**: `pandoc output/*.md -o "book.docx" --toc`

## 🔧 Requirements

- Python 3.7+
- `google-generativeai` library (`pip install google-generativeai`)
- Pandoc (for final compilation)
- Google AI Studio API key

## 💡 Tips for Better Results

1. **Detailed Outlines**: More detail = better content
2. **Consistent Tone**: Keep your tone description specific
3. **Character Sheets**: Include character descriptions in your outline
4. **Chapter Flow**: Ensure logical progression between chapters
5. **Genre Specificity**: Be specific about your genre and target audience

## 🚨 Important Notes

- The script includes rate limiting (2-second delays between API calls)
- Failed generations are retried up to 3 times
- Each chapter maintains context from previous chapters
- Generated files are numbered for proper compilation order

## 📄 License

This project is open source. Customize and use as needed for your eBook projects.

---

**Happy Writing! 📝✨**