from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from fastapi.responses import JSONResponse
from pymongo.collection import Collection
from slugify import slugify

from libs.connet_db import get_collection
from models.admin_models import CreatePost

router = APIRouter()


@router.post(
    "/upload",
    # response_model=CreatePost,
    response_description="Create a new post",
    status_code=status.HTTP_201_CREATED,
    # response_model_by_alias=False,
)
async def upload_post(
    request: Request, collection: Collection = Depends(get_collection)
):

    form_data = await request.form()
    file = form_data.get("file")
    title = form_data.get("title")
    category = form_data.get("category")
    tags = form_data.get("tags")
    created_at = form_data.get("createdAt")
    modified_at = datetime.now().strftime("%y-%m-%d-%H:%M")
    # 异步读取文件内容
    file_contents = await file.read()

    # 将字节转换为字符串
    file_contents_str = file_contents.decode("utf-8")

    # 创建要插入的文档
    post_data = {
        "title": title,
        "slug": slugify(title),
        "category": category,
        "tags": tags.split(",") if tags else [],
        "content": file_contents_str,
        "created_at": created_at,
        "modified_at": modified_at,
    }
    existing_post = await collection.find_one({"slug": post_data["slug"]})
    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A post with the title '{title}' already exists.",
        )

    # 将文档插入到 MongoDB
    result = await collection.insert_one(post_data)

    # 获取插入的文档的 ID
    post_id = str(result.inserted_id)

    # 返回创建的文章数据
    response_data = {"title": post_data["title"], "_id": post_id}
    return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


@router.get("/articles", response_description="Get all articles")
async def get_articles(collection: Collection = Depends(get_collection)):
    articles = []
    async for article in collection.find(
        {},
        {
            "created_at": 1,
            "modified_at": 1,
            "title": 1,
            "category": 1,
            "tags": 1,
            "_id": 0,
        },
    ):
        articles.append(article)
    return JSONResponse(content=articles)
