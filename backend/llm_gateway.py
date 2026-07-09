import os
import time
from dotenv import load_dotenv
import google.genai as genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def should_retry(error) -> bool:
    status_code = getattr(error, "code", None)
    return status_code in {429, 500, 502, 503, 504}

def get_llm_response(structured_prompt: str) -> str:
    # 1. Swap to 1.5-flash for the massive free tier limits
    model_name = "gemini-1.5-flash"
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
            if not should_retry(e):
                # Shield the frontend from non-rate-limit crashes
                print(f"Non-retryable error: {e}")
                return "My circuits got a bit crossed trying to read that. Could you rephrase your answer?"

            if attempt == max_retries - 1:
                print(f"Gemini API failed permanently after {max_retries} attempts.")
                # 2. Return a safe string to the UI instead of crashing the server
                return "I'm experiencing a bit of heavy traffic right now! Give me about 30 seconds to catch my breath and hit send again."
            
            delay = initial_delay * (2 ** attempt)
            status = getattr(e, "code", "Unknown")
            print(f"Gemini overloaded (Status {status}). Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)