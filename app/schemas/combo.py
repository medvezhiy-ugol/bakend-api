from pydantic import BaseModel
from typing import List
from beanie import Document
from uuid import UUID


class Product(BaseModel):
    productId: UUID
    sizeId: UUID
    forbiddenModifiers: List[UUID]
    priceModificationAmount: int


class Group(Document):
    id: UUID # такой же как в comboCategories
    name: str
    isMainGroup: bool
    products: List[Product]


class ComboSpecification(BaseModel):
    sourceActionId: UUID
    categoryId: UUID
    name: str
    priceModificationType: int
    priceModification: int
    isActive: bool
    startDate: str
    expirationDate: str
    lackingGroupsToSuggest: int
    includeModifiers: bool
    groups: List[Group]

class Warning(BaseModel):
    Code: str
    Message: str


class ComboCategorie(Document):
    id :UUID
    name: str

class Combo(Document):
    comboSpecifications : List[ComboSpecification]
    comboCategories: List[ComboCategorie]
    Warnings: List[Warning]
    
class ComboCredits(BaseModel):
    organizationId: UUID