from fastapi import Request
from pymongo.collection import Collection


def get_collection(request: Request, collection_name: str ='blog') -> Collection:
        return request.app.mongodb[collection_name]