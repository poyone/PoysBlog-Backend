import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# 定义 JWT 相关的配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7200


# 创建 OAuth2 密码验证器
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

# 创建密码哈希器
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 验证用户凭据
def authenticate_user(username: str, password: str):
    env_user = os.environ.get('USER_NAME')
    user = username == env_user
    
    if not user:
        return False
    if not pwd_context.verify(password, os.environ.get('HASHED_PASSWORD')):
        return False
    return {'username':env_user}

# 生成 JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证 JWT
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    env_user = os.environ.get('USER_NAME')
    user = username == env_user
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {'username':env_user}


