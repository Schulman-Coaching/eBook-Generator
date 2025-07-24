import google.generativeai as genai
import json

# Load the API key from config
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Configure Gemini with your API key
genai.configure(api_key=config['gemini_api_key'])

print("Available Gemini models:")
print("=" * 50)

try:
    for model in genai.list_models():
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Input Token Limit: {model.input_token_limit}")
        print(f"  Output Token Limit: {model.output_token_limit}")
        print(f"  Supported Generation Methods: {model.supported_generation_methods}")
        print("-" * 40)
except Exception as e:
    print(f"Error listing models: {e}")