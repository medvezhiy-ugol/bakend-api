from pydantic import BaseModel
from uuid import UUID
from beanie import Document, Link
from typing import List, Optional


class MenuCredits(BaseModel):
    organizationIds: UUID
    externalMenuId: int


class taxCategoryModel(BaseModel):
    id: str
    name: str
    percentage: int


class allergenGroupModel(BaseModel):
    id: UUID
    code: str
    name: str


class priceModel(BaseModel):
    organizationId: str
    price: float


class RestrictionsModel(BaseModel):
    minQuantity: int
    maxQuantity: int
    freeQuantity: int
    byDefault: int


class tagModel(BaseModel):
    id: str
    name: str


class ItemsModel(BaseModel):
    prices: List[priceModel] | None
    sku: str
    name: str
    description: str
    buttonImage: str | None
    restrictions: RestrictionsModel
    allergenGroups: List[allergenGroupModel] | None
    nutritionPerHundredGrams: Optional[dict]
    portionWeightGrams: float
    tags: List[tagModel]
    itemId: UUID


class itemModifierGroupModel(BaseModel):
    items: List[ItemsModel] | None
    name: str
    description: str
    restrictions: RestrictionsModel
    canBeDivided: bool
    itemGroupId: UUID
    childModifiersHaveMinMaxRestrictions: bool
    sku: str


class itemSizeModel(BaseModel):
    prices: List[priceModel] | None
    itemModifierGroups: List[itemModifierGroupModel] | None
    sku: str
    sizeCode: Optional[str]
    sizeName: Optional[str]
    isDefault: bool
    portionWeightGrams: int
    sizeId: Optional[UUID]
    nutritionPerHundredGrams: Optional[dict]
    buttonImageUrl: Optional[str] 
    buttonImageCroppedUrl: dict | None


class ItemModel(Document):
    itemSizes: List[itemSizeModel]
    sku: str
    name: str
    description: str
    allergenGroups: List[allergenGroupModel] | None
    itemId: UUID
    modifierSchemaId: UUID
    taxCategory: taxCategoryModel
    orderItemType: str
    modifierSchemaId: Optional[UUID]


class ItemCategorie(BaseModel):
    items: List[Link[ItemModel]]
    id: UUID
    name: str
    description: str
    buttonImageUrl: str | None
    headerImageUrl: str | None
    iikoGroupId: UUID


class MenuResponse(Document):
    id: int
    name: str
    description: str
    itemCategories: List[ItemCategorie]
    comboCategories: list
