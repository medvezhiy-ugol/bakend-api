from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField
from uuid import UUID


class Organization(BaseModel):
    id: ObjectIdField = None
    responseType: str
    name: str

    class Config:
        # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectId: str}


