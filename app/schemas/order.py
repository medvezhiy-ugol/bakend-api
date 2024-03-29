from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from beanie import Document

class ComboInformationModel(BaseModel):
    comboId: UUID
    comboSourceId: UUID
    comboGroupId: UUID


class ItemsModel(BaseModel):
    type: str
    amount: int
    productSizeId: UUID | None
    productId: UUID
    comboInformation: ComboInformationModel | None
    comment: str | None
    price: int


class GuestsModel(BaseModel):
    count: int


class CustomerModel(BaseModel):
    id: UUID
    name: str
    surname: str | None
    comment: str
    birthdate: str | None  # ПОФИКСИТЬ ПРИ ТЕСТАХ
    email: str | None
    shouldReceivePromoActionsInfo: bool | None
    shouldReceiveOrderStatusNotifications: bool | None
    # gender: ???????????????????????????????????????????????????
    type: str | None


class TableIdsModel(BaseModel):
    id: UUID


class CombosModel(BaseModel):
    id: UUID
    name: str
    amount: int
    price: int
    sourceId: UUID
    programId: UUID


class PaymentAdditionalDataModel(BaseModel):
    credential: str 
    searchScope: str
    type: str


class PaymentsModel(BaseModel):
    paymentTypeKind: str
    sum: int
    paymentTypeId: UUID
    isProcessedExternally: bool | None
    paymentAdditionalData: PaymentAdditionalDataModel | None
    isFiscalizedExternally: bool | None


class TipsModel(BaseModel):
    paymentTypeKind: str
    tipsTypeId: UUID
    sum: int
    paymentTypeId: UUID
    isProcessedExternally: bool
    paymentAdditionalData: PaymentAdditionalDataModel | None
    isFiscalizedExternally: bool


class CardModel(BaseModel):
    track: str


class DiscountsModel(BaseModel):
    type: str


class DiscountsInfoModel(BaseModel):
    card: CardModel
    discounts: List[DiscountsModel]


class IikoCard5InfoModel(BaseModel):
    coupon: str
    applicableManualConditions: List[UUID]


class OrderDraft(BaseModel):
    menuId = "11672"
    id: UUID | None
    externalNumber: str | None
    tableIds: List[TableIdsModel] | None
    customer: CustomerModel | None
    phone: str | None
    guests: GuestsModel | None
    tabName: str | None
    items: List[ItemsModel]
    combos: List[CombosModel] | None
    payments: List[PaymentsModel]
    tips: List[TipsModel] | None
    sourceKey: str | None
    discountsInfo: DiscountsInfoModel | None
    iikoCard5Info: IikoCard5InfoModel | None
    orderTypeId: UUID

class Street(BaseModel):
    name: str
    city: str

class DeliveryAddress(BaseModel):
    street: Street
    house: str

class Delivery(BaseModel):
    address: DeliveryAddress
    comment: str | None
    
class Order(BaseModel):
    id: UUID | None
    completeBefore: str | None
    externalNumber: str | None
    tableIds: List[TableIdsModel] | None
    customer: CustomerModel | None
    phone: str | None
    guests: GuestsModel | None
    tabName: str | None
    items: List[ItemsModel]
    combos: List[CombosModel] | None
    payments: List[PaymentsModel]
    tips: List[TipsModel] | None
    sourceKey: str | None
    discountsInfo: DiscountsInfoModel | None
    iikoCard5Info: IikoCard5InfoModel | None
    orderTypeId: UUID
    deliveryPoint:Delivery | None



    
class createOrderSettingsModel(BaseModel):
    transportToFrontTimeout: int


class OrderCreate(BaseModel):
    organizationId: UUID
    terminalGroupId: UUID
    order: Order
    createOrderSettings: createOrderSettingsModel | None


class ErrorInfoModel(BaseModel):
    code: str


class OrderInfoModel(BaseModel):
    id: UUID
    posId: UUID | None
    externalNumber: str | None
    organizationId: UUID
    timestamp: int
    creationStatus: str
    errorInfo: ErrorInfoModel | None
    order: Order | None


class OrderResponsePydantic(BaseModel):
    correlationId: UUID
    orderInfo: OrderInfoModel

class OrderResponse(Document):
    id: UUID
    user_id: str
    orderInfo: OrderInfoModel


class OrderCreateDraft(BaseModel):
    organizationId: UUID
    terminalGroupId: UUID
    order: OrderDraft
    createOrderSettings: createOrderSettingsModel | None
    createdAt: str | None
    lockedByUser: str | None
    employeeId: str  | None

class TinkoffRequest(BaseModel):
    TerminalKey: str
    OrderId: str
    Success: bool
    Amount: int
    Token: str
    PaymentId: str