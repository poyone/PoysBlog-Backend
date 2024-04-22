from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

# 定义 JWT 相关的配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 定义 Pydantic 模型,用于请求体和响应体
class User(BaseModel):
    username: str
    password: str

# 创建 OAuth2 密码验证器
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 创建密码哈希器
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "secret"
hashed_password = pwd_context.hash(password)
print(hashed_password)

# 模拟一个用户数据库
users_db = {
    "john": {
        "username": "john",
        "hashed_password": f"{hashed_password}",
    }
}

# 验证用户凭据
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return False
    if not pwd_context.verify(password, user["hashed_password"]):
        return False
    return user

# 生成 JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
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
    user = users_db.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

# 登录接口
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 受保护的接口示例
@app.get("/protected")
def protected_route(current_user: User = Depends(verify_token)):
    return {"message": f"Hello, {current_user['username']}! This is a protected route."}

if __name__ == "__main__":
    import uvicorn    
    uvicorn.run("demo_of_jwt:app", port=2333, reload=True)