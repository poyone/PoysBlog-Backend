from typing import List, Optional

from bson import ObjectId
from exceptiongroup import catch
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.responses import JSONResponse
from pymongo import ReturnDocument
from pymongo.collection import Collection
from slugify import slugify

from libs.connet_db import get_collection
from models.blog_models import Post

router = APIRouter()


@router.get("/", response_description="List latest Articles")
async def get_latest_articles(collection: Collection = Depends(get_collection)):
    pipeline = [
        {"$match": {"category": {"$in": ["Frontend", "Backend", "Cloud"]}}},
        {"$sort": {"modified_at": -1}},
        {"$group": {"_id": "$category", "titles": {"$push": "$title"}}},
        {
            "$project": {
                "_id": 0,
                "category": "$_id",
                "titles": {"$slice": ["$titles", 2]},
            }
        },
        {"$sort": {"category": 1}}
    ]
    cursor = collection.aggregate(pipeline)
    try:
        response = [el async for el in cursor]
        return JSONResponse(content={"content":response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories", response_description="Get all categories")
async def get_categories(collection: Collection = Depends(get_collection)):
    category_pipeline = [
        {"$group": {"_id": "$category"}},
        {"$project": {"_id": 0, "category": "$_id"}},
    ]
    category_cursor = collection.aggregate(category_pipeline)

    # 获取所有文章的指定信息
    article_pipeline = [
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "category": 1,
                "tags": 1,
                "created_at": 1,
                "modified_at": 1,
            }
        }
    ]
    article_cursor = collection.aggregate(article_pipeline)

    try:
        categories_info = [el async for el in category_cursor]
        articles_info = [el async for el in article_cursor]
        return JSONResponse(
            content={"categories": categories_info, "article_items": articles_info}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{title}",
    response_model=Post,
    response_description="Get target post",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def get_posts(title: str, collection: Collection = Depends(get_collection)):

    slug = slugify(title)
    if (post := await collection.find_one({"slug": slug})) is not None:
        return post

    raise HTTPException(status_code=404, detail=f"Post {title} not found")
