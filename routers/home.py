from typing import List, Optional

from bson import ObjectId
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from pymongo import ReturnDocument
from pymongo.collection import Collection

from models.blog import Post

router = APIRouter()
def get_collection(request: Request, collection_name: str ='blog') -> Collection:
        return request.app.mongodb[collection_name]
    
    
@router.get("/{title}", 
            response_model=Post,
            response_description="List all posts",
            status_code=status.HTTP_200_OK,
            response_model_by_alias=False)
async def get_posts(title:str, collection: Collection = Depends(get_collection)):
    
    slug = title.lower().replace(' ', '-')
    if (
        post := await collection.find_one({'slug': slug})
    ) is not None:
        return post
    
    raise HTTPException(status_code=404,
                        detail=f'Post {title} not found')