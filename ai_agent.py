
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
else:
    client = OpenAI(api_key=api_key)
    print("MetricMind AI Agent setup successful!")
