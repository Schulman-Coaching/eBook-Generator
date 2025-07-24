import os
import json
import re
import time
import google.generativeai as genai

# --- Configuration and Setup ---

def load_config(config_path='config.json'):
    """Loads configuration from a JSON file."""
    print("Loading configuration...")
    with open(config_path, 'r') as f:
        return json.load(f)

def setup_gemini(api_key):
    """Configures the Gemini API client."""
    print("Initializing Gemini API...")
    genai.configure(api_key=api_key)
    # Using a model optimized for longer, creative text generation
    return genai.GenerativeModel('gemini-1.5-flash-latest')

def parse_outline(filepath):
    """Parses the outline file to extract chapter titles."""
    print(f"Parsing outline file: {filepath}...")
    try:
        with open(filepath, 'r') as f:
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
    """Creates the output directory if it doesn't exist."""
    print(f"Ensuring output directory '{path}' exists...")
    os.makedirs(path, exist_ok=True)
    return path

# --- Content Generation ---

def generate_content(prompt, model, attempt=1, max_attempts=3):
    """Generates content using the Gemini API with a retry mechanism."""
    try:
        response = model.generate_content(prompt)
        # Add a small delay to respect API rate limits
        time.sleep(2)
        return response.text
    except Exception as e:
        print(f"Error during API call (Attempt {attempt}/{max_attempts}): {e}")
        if attempt < max_attempts:
            print("Retrying in 5 seconds...")
            time.sleep(5)
            return generate_content(prompt, model, attempt + 1, max_attempts)
        else:
            print("Max retry attempts reached. Skipping this part.")
            return None

def generate_front_matter(config, model, output_dir):
    """Generates title page, copyright, and dedication."""
    print("Generating front matter...")
    
    # Title Page
    prompt = f"Generate the text for a standard book title page. Title: '{config['book_title']}', Subtitle: '{config['subtitle']}', Author: '{config['author_name']}'."
    content = generate_content(prompt, model)
    if content:
        with open(os.path.join(output_dir, '00_title_page.md'), 'w') as f:
            f.write(content)

    # Copyright Page
    current_year = time.strftime("%Y")
    prompt = f"Generate a standard copyright page for a book. Author: '{config['author_name']}', Year: '{current_year}'. Include a generic 'All rights reserved' clause."
    content = generate_content(prompt, model)
    if content:
        with open(os.path.join(output_dir, '01_copyright.md'), 'w') as f:
            f.write(content)

    # Dedication Page
    prompt = f"Generate a heartfelt dedication for a book in the '{config['genre']}' genre with a '{config['tone']}' tone."
    content = generate_content(prompt, model)
    if content:
        with open(os.path.join(output_dir, '02_dedication.md'), 'w') as f:
            f.write(content)
            
    print("Front matter generated.")

def generate_chapters(config, chapters, model, output_dir):
    """Generates each chapter based on the outline."""
    print("Generating chapters...")
    full_outline = "\n".join(f"## {title}" for title in chapters)
    previous_chapter_summary = "This is the first chapter of the book."

    for i, title in enumerate(chapters):
        chapter_number = i + 1
        print(f"  - Generating Chapter {chapter_number}: {title}")

        prompt = f"""
        You are an expert author writing a book titled "{config['book_title']}" by {config['author_name']}.
        The book's genre is '{config['genre']}' and the tone should be '{config['tone']}'.
        The target audience is '{config['target_audience']}'.

        You are now writing Chapter {chapter_number}, titled "{title}".
        This chapter should be approximately {config['word_count_per_chapter']} words.
        
        CONTEXT:
        - Summary of previous chapter: {previous_chapter_summary}
        - Full Book Outline:
        {full_outline}
        
        INSTRUCTIONS:
        - Write the full body content for this chapter.
        - Ensure a logical flow from the previous chapter summary.
        - Conclude the chapter in a way that sets up the next one.
        - IMPORTANT: Do NOT include the chapter title (like 'Chapter 1: ...') in your output. Only provide the chapter's body text.
        
        Begin writing now.
        """
        
        content = generate_content(prompt, model)
        if content:
            filename = f"{i+3:02d}_chapter_{chapter_number}.md"
            with open(os.path.join(output_dir, filename), 'w') as f:
                f.write(content)
            
            # Generate a summary of the chapter we just wrote for the next iteration
            summary_prompt = f"Summarize the following text in one or two sentences for context in a book authoring AI: {content[:1000]}"
            previous_chapter_summary = generate_content(summary_prompt, model) or "No summary available."
        else:
            print(f"    Failed to generate content for Chapter {chapter_number}.")
            previous_chapter_summary = "Could not generate previous chapter, so context is missing."
            
    print("All chapters generated.")

def generate_back_matter(config, model, output_dir, final_chapter_number):
    """Generates the 'About the Author' section."""
    print("Generating back matter...")
    
    # About the Author
    prompt = f"Write an 'About the Author' section for {config['author_name']}. Invent a plausible professional background related to the book's topic of '{config['genre']}'. The tone should be professional yet approachable. Aim for about 150 words."
    content = generate_content(prompt, model)
    if content:
        filename = f"{final_chapter_number + 3:02d}_about_the_author.md"
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write(content)
            
    print("Back matter generated.")

# --- Main Execution ---

def main():
    """Main function to run the ebook generation process."""
    try:
        config = load_config()
        if not config.get("gemini_api_key") or config["gemini_api_key"] == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            print("Error: Gemini API key is missing from config.json.")
            return

        model = setup_gemini(config['gemini_api_key'])
        chapters = parse_outline(config['outline_file'])
        
        if chapters is None:
            return

        output_dir = create_output_directory()

        generate_front_matter(config, model, output_dir)
        generate_chapters(config, chapters, model, output_dir)
        generate_back_matter(config, model, output_dir, len(chapters))

        print("\n" + "="*50)
        print("✅ EBOOK GENERATION COMPLETE!")
        print(f"All files have been saved in the '{output_dir}' directory.")
        print("="*50 + "\n")
        print("NEXT STEP: Compile your ebook using Pandoc.")
        print("1. Open a terminal or command prompt.")
        print(f"2. Navigate to your project directory: cd path/to/your/project")
        print("3. Run the following command:")
        print(f'   pandoc output/*.md -o "{config["book_title"]}.epub" --toc --metadata title="{config["book_title"]}" --metadata creator="{config["author_name"]}"')
        
    except FileNotFoundError:
        print("Error: 'config.json' not found. Please ensure it exists in the same directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()