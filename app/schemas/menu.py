from pydantic import BaseModel
from beanie import Document, Link
from typing import List, Optional


class NewUuid(str):
    """
    Partial UK postcode validation. Note: this is just an example, and is not
    intended for use in production; in particular this does NOT guarantee
    a postcode exists, just that it has a valid format.
    """

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern='^[A-F0-9a-f]{8}(-[A-F0-9a-f]{4}){3}-[A-F0-9a-f]{12}$',
            # some example postcodes
            examples=['4a33135d-8aa3-47ba-bcfd-faa297b7fb5b'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(f'{v}')

    def __repr__(self):
        return f'NewUuid({super().__repr__()})'


class MenuCredits(BaseModel):
    organizationIds: NewUuid
    externalMenuId: int


class taxCategoryModel(BaseModel):
    id: str
    name: str
    percentage: int


class allergenGroupModel(BaseModel):
    id: NewUuid
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
    itemId: NewUuid


class itemModifierGroupModel(BaseModel):
    items: List[ItemsModel] | None
    name: str
    description: str
    restrictions: RestrictionsModel
    canBeDivided: bool
    itemGroupId: NewUuid
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
    sizeId: Optional[NewUuid]
    nutritionPerHundredGrams: Optional[dict]
    buttonImageUrl: Optional[str]
    buttonImageCroppedUrl: dict | None


class ItemModel(Document):
    itemSizes: List[itemSizeModel]
    sku: str
    name: str
    description: str
    allergenGroups: List[allergenGroupModel] | None
    itemId: NewUuid
    modifierSchemaId: NewUuid
    taxCategory: taxCategoryModel | None
    orderItemType: str
    modifierSchemaId: Optional[NewUuid]
    # id itemCategorie


class ItemCategorie(Document):
    items: List[Link[ItemModel]]
    id: NewUuid
    name: str
    description: str
    buttonImageUrl: str | None
    headerImageUrl: str | None
    iikoGroupId: NewUuid | None


class MenuResponse(Document):
    id: int
    name: str
    description: str
    itemCategories: List[Link[ItemCategorie]]
    comboCategories: list
