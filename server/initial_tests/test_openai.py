# test_openai.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Check if API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY not found in .env file")
    exit(1)

print(f"API key loaded: {api_key[:20]}...")

try:
    # Create OpenAI client (newer API approach)
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello! Can you respond with just 'Princeton Chatbot Test Successful'?"}],
        max_tokens=20
    )
    print("OpenAI API connection successful!")
    print(f"Model used: gpt-4o-mini")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"OpenAI API connection failed: {e}")
    print(f"Error type: {type(e).__name__}")