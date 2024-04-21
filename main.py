from contextlib import asynccontextmanager

from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from routers.admin import router as admin_router
from routers.home import router as post_router

DB_URL = config('DB_URL', cast=str)
DB_NAME = config('DB_NAME', cast=str)

# define origins
origins = ["*"]

@asynccontextmanager
async def db_client_lifespan(app: FastAPI):
    # 在这里创建数据库连接
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    yield
    # 关闭数据库连接
    app.mongodb_client.close()

# instantiate the app
app = FastAPI(lifespan=db_client_lifespan)

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router, prefix="/blog", tags=["blog"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])

if __name__ == "__main__":
    import uvicorn    
    uvicorn.run("main:app", port=2333, reload=True)