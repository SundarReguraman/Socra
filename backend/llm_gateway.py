import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_llm_response(structured_prompt: str) -> str:
    response = model.generative_content(structured_prompt)
    return response.text