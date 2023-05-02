from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField
from beanie import Document
from uuid import UUID


class Organization(Document):
    id: UUID = None
    responseType: str
    name: str
    longitude: float
    latitude: float
    restaurantAddress: str

