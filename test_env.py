import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the values from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

print(f"OpenAI API Key: {OPENAI_API_KEY}")
