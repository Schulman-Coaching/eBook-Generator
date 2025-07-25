"""
Content generation functionality for the eBook Generator.
"""

import os
import time


class ContentGenerator:
    """Handles AI-powered content generation for eBooks."""
    
    def __init__(self, model, config):
        """Initialize the content generator.
        
        Args:
            model: Configured Gemini model instance
            config (dict): Configuration dictionary
        """
        self.model = model
        self.config = config
    
    def generate_content(self, prompt, attempt=1, max_attempts=3):
        """Generates content using the Gemini API with a retry mechanism.
        
        Args:
            prompt (str): The prompt to send to the AI
            attempt (int): Current attempt number
            max_attempts (int): Maximum number of retry attempts
            
        Returns:
            str: Generated content, or None if all attempts failed
        """
        try:
            response = self.model.generate_content(prompt)
            # Add a small delay to respect API rate limits
            time.sleep(2)
            return response.text
        except Exception as e:
            print(f"Error during API call (Attempt {attempt}/{max_attempts}): {e}")
            if attempt < max_attempts:
                print("Retrying in 5 seconds...")
                time.sleep(5)
                return self.generate_content(prompt, attempt + 1, max_attempts)
            else:
                print("Max retry attempts reached. Skipping this part.")
                return None
    
    def generate_front_matter(self, output_dir):
        """Generates title page, copyright, and dedication.
        
        Args:
            output_dir (str): Directory to save generated files
        """
        print("Generating front matter...")
        
        # Title Page
        prompt = f"Write only the text content for a standard book title page. Title: '{self.config['book_title']}', Subtitle: '{self.config['subtitle']}', Author: '{self.config['author_name']}'. Do not include any commentary, options, or explanations. Provide only the formatted title page content."
        content = self.generate_content(prompt)
        if content:
            with open(os.path.join(output_dir, '00_title_page.md'), 'w', encoding='utf-8') as f:
                f.write(content)

        # Copyright Page
        current_year = time.strftime("%Y")
        prompt = f"Write only the text content for a standard copyright page for a book. Author: '{self.config['author_name']}', Year: '{current_year}'. Include a generic 'All rights reserved' clause. Do not include any commentary or explanations. Provide only the copyright page content."
        content = self.generate_content(prompt)
        if content:
            with open(os.path.join(output_dir, '01_copyright.md'), 'w', encoding='utf-8') as f:
                f.write(content)

        # Dedication Page
        prompt = f"Write only the text content for a heartfelt dedication for a book in the '{self.config['genre']}' genre with a '{self.config['tone']}' tone. Do not include any commentary or explanations. Provide only the dedication content."
        content = self.generate_content(prompt)
        if content:
            with open(os.path.join(output_dir, '02_dedication.md'), 'w', encoding='utf-8') as f:
                f.write(content)
                
        print("Front matter generated.")
    
    def generate_chapters(self, chapters, output_dir):
        """Generates each chapter based on the outline.
        
        Args:
            chapters (list): List of chapter titles
            output_dir (str): Directory to save generated files
        """
        print("Generating chapters...")
        full_outline = "\n".join(f"## {title}" for title in chapters)
        previous_chapter_summary = "This is the first chapter of the book."

        for i, title in enumerate(chapters):
            chapter_number = i + 1
            print(f"  - Generating Chapter {chapter_number}: {title}")

            prompt = f"""
            You are an expert author writing a book titled "{self.config['book_title']}" by {self.config['author_name']}.
            The book's genre is '{self.config['genre']}' and the tone should be '{self.config['tone']}'.
            The target audience is '{self.config['target_audience']}'.

            You are now writing Chapter {chapter_number}, titled "{title}".
            This chapter should be approximately {self.config.get('word_count_per_chapter', 2500)} words.
            
            CONTEXT:
            - Summary of previous chapter: {previous_chapter_summary}
            - Full Book Outline:
            {full_outline}
            
            INSTRUCTIONS:
            - Write the full body content for this chapter.
            - Ensure a logical flow from the previous chapter summary.
            - Conclude the chapter in a way that sets up the next one.
            - IMPORTANT: Do NOT include the chapter title (like 'Chapter 1: ...') in your output. Only provide the chapter's body text.
            - Do NOT include any meta-commentary, AI thinking, or phrases like "Of course", "Here are options", or "I'll provide".
            - Write directly as the author would, with no AI assistant commentary or explanations.
            - Start immediately with the chapter content, no preamble or setup text.
            
            Begin writing the chapter content now.
            """
            
            content = self.generate_content(prompt)
            if content:
                filename = f"{i+3:02d}_chapter_{chapter_number}.md"
                with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Generate a summary of the chapter we just wrote for the next iteration
                summary_prompt = f"Summarize the following text in one or two sentences for context in a book authoring AI: {content[:1000]}"
                previous_chapter_summary = self.generate_content(summary_prompt) or "No summary available."
            else:
                print(f"    Failed to generate content for Chapter {chapter_number}.")
                previous_chapter_summary = "Could not generate previous chapter, so context is missing."
                
        print("All chapters generated.")
    
    def generate_back_matter(self, output_dir, final_chapter_number):
        """Generates the 'About the Author' section.
        
        Args:
            output_dir (str): Directory to save generated files
            final_chapter_number (int): Number of the final chapter
        """
        print("Generating back matter...")
        
        # About the Author - Use specific biography for Elie Schulman
        elie_bio = """# About the Author: Elie Schulman

A Note from Elie Schulman: The words within this book, like all human expressions, are not claimed to be "true" in any absolute or immutable sense. They represent a perspective, a synthesis of observations, and a framework for understanding, offered with the hope that they spark your own insights and questions.

Elie Schulman is a writer and explorer of human consciousness and emerging technologies, dedicated to understanding how we better articulate our desires in an ever-changing world. His lifelong fascination with language and words has been a constant thread, weaving through diverse experiences that shaped his unique perspective.

In April 2024, Elie had his first significant interaction with ChatGPT. The experience was immediate and profound, an uncanny sensation of "looking in the mirror" – a reflection not just of synthesized knowledge, but of the very structure of human thought and communication. This moment solidified an intuition that AI would fundamentally shift our understanding of ourselves.

Elie's journey through language and communication includes:

- Years of rigorous Talmud study, delving into the nuanced interpretations and precise articulations of ancient texts.
- Years of practicing law, where every word, every phrase, and every question held immense consequence in shaping outcomes.
- Decades of consistent journaling, a private practice of self-prompting and continuous refinement of thought.
- Decades of sitting practice of meditation, cultivating deep awareness of internal states and the subtle interplay of mind and experience.
- Decades immersed in interpersonal process groups, honing the delicate art of expressing needs, hearing others, and navigating complex human dynamics.

These rich experiences fueled an immediate realization upon encountering advanced AI: humanity was on the cusp of at least two profound awakenings. The first, concerning work and economics, signaling a redefinition of labor, value, and societal structures. The second, and perhaps more significantly, relating to human value and spirituality, prompting a deeper inquiry into what truly defines us when machines can mimic so much of our intellect.

Driven by the belief that clear and intentional communication is the bedrock of all progress, Elie wrote "Prompting: Humans Learning How to Ask For What They Want" to empower individuals and organizations to navigate the complexities of the AI era with confidence and precision. His work focuses on demystifying complex concepts and providing practical, actionable insights that can be applied in both professional and personal contexts.

When not writing or researching, Elie enjoys spending time with his family, skiing and tennis."""
        
        filename = f"{final_chapter_number + 3:02d}_about_the_author.md"
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
            f.write(elie_bio)
                
        print("Back matter generated.")