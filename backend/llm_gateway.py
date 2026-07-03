import os
import time
from dotenv import load_dotenv
import google.genai as genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def get_llm_response(structured_prompt: str) -> str:
    model_name = "gemini-2.5-flash"
    max_retries = 3
    initial_delay = 2

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=structured_prompt
            )
            return response.text
            
        except (errors.APIError, errors.ClientError) as e:
            # If it's the last attempt, raise the error to be handled by your endpoint
            if attempt == max_retries - 1:
                print(f"Gemini API failed permanently after {max_retries} attempts.")
                raise e
            
            # Calculate backoff delay (e.g., 2s, 4s, 8s) to give the server breathing room
            delay = initial_delay * (2 ** attempt)
            print(f"Gemini overloaded or rate-limited (Status {e.code}). Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)