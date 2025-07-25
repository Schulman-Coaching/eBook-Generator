"""
Main eBook Generator class that orchestrates the entire generation process.
"""

from .config import load_config, setup_gemini, validate_config
from .utils import parse_outline, create_output_directory
from .content import ContentGenerator


class EbookGenerator:
    """Main class for generating eBooks using AI."""
    
    def __init__(self, config_path='config.json'):
        """Initialize the eBook generator.
        
        Args:
            config_path (str): Path to the configuration file
        """
        self.config_path = config_path
        self.config = None
        self.model = None
        self.content_generator = None
    
    def load_configuration(self):
        """Load and validate the configuration."""
        try:
            self.config = load_config(self.config_path)
            validate_config(self.config)
            return True
        except (FileNotFoundError, ValueError) as e:
            print(f"Configuration error: {e}")
            return False
    
    def initialize_ai_model(self):
        """Initialize the AI model."""
        try:
            self.model = setup_gemini(self.config['gemini_api_key'])
            self.content_generator = ContentGenerator(self.model, self.config)
            return True
        except Exception as e:
            print(f"Error initializing AI model: {e}")
            return False
    
    def generate_ebook(self, output_dir='output'):
        """Generate the complete eBook.
        
        Args:
            output_dir (str): Directory to save generated files
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load configuration
            if not self.load_configuration():
                return False
            
            # Initialize AI model
            if not self.initialize_ai_model():
                return False
            
            # Parse outline
            chapters = parse_outline(self.config['outline_file'])
            if chapters is None:
                return False
            
            # Create output directory
            output_path = create_output_directory(output_dir)
            
            # Generate content
            self.content_generator.generate_front_matter(output_path)
            self.content_generator.generate_chapters(chapters, output_path)
            self.content_generator.generate_back_matter(output_path, len(chapters))
            
            # Success message
            print("\n" + "="*50)
            print("✅ EBOOK GENERATION COMPLETE!")
            print(f"All files have been saved in the '{output_path}' directory.")
            print("="*50 + "\n")
            print("NEXT STEP: Compile your ebook using Pandoc.")
            print("1. Open a terminal or command prompt.")
            print(f"2. Navigate to your project directory: cd path/to/your/project")
            print("3. Run the following command:")
            print(f'   pandoc {output_dir}/*.md -o "{self.config["book_title"]}.epub" --toc --metadata title="{self.config["book_title"]}" --metadata creator="{self.config["author_name"]}"')
            
            return True
            
        except Exception as e:
            print(f"An unexpected error occurred during eBook generation: {e}")
            return False
    
    def get_book_info(self):
        """Get information about the book being generated.
        
        Returns:
            dict: Book information or None if config not loaded
        """
        if not self.config:
            return None
        
        return {
            'title': self.config.get('book_title'),
            'subtitle': self.config.get('subtitle'),
            'author': self.config.get('author_name'),
            'genre': self.config.get('genre'),
            'target_audience': self.config.get('target_audience'),
            'tone': self.config.get('tone'),
            'word_count_per_chapter': self.config.get('word_count_per_chapter', 2500)
        }
    
    def preview_chapters(self):
        """Preview the chapters that will be generated.
        
        Returns:
            list: List of chapter titles or None if outline not found
        """
        if not self.config:
            if not self.load_configuration():
                return None
        
        return parse_outline(self.config['outline_file'])


def main():
    """Main function to run the ebook generation process."""
    generator = EbookGenerator()
    success = generator.generate_ebook()
    
    if not success:
        print("eBook generation failed. Please check the error messages above.")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())