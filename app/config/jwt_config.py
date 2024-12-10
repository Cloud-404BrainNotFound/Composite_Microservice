from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import configparser

# Read config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# JWT Configuration from config.ini
JWT_SECRET_KEY = config['jwt']['secret_key']
JWT_ALGORITHM = config['jwt']['algorithm']
JWT_EXPIRE_MINUTES = int(config['jwt']['expire_minutes'])

security = HTTPBearer()

def create_access_token(user_data: dict) -> str:
    """Create JWT access token"""
    expires_delta = timedelta(minutes=JWT_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "sub": str(user_data.get("user_id")),
        "email": user_data.get("email"),
        "role": user_data.get("role"),
        "exp": expire
    }
    
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Validate JWT token and return user information"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Check token expiration
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token is missing expiration")
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")
            
        # Return user information from token
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role")
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=f"Could not validate credentials: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}") 