from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import configparser

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

JWT_SECRET_KEY = config['jwt']['secret_key']
JWT_ALGORITHM = config['jwt']['algorithm']
JWT_EXPIRE_MINUTES = int(config['jwt']['expire_minutes'])

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token") 