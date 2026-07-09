import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()
security = HTTPBearer()

def verify_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Catches the JWT token from the frontend, verifies it using the Supabase secret,
    and extracts the user's UUID.
    """
    token = credentials.credentials
    try:
        # We use your Supabase secret key to verify the token isn't forged
        payload = jwt.decode(
            token, 
            os.getenv("SUPABASE_JWT_SECRET"), 
            algorithms=["HS256"],
            audience="authenticated"
        )
        # "sub" (subject) is standard JWT terminology for the user's ID
        return payload["sub"] 
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")