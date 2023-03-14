from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ComboInformationModel(BaseModel):
    comboId: UUID
    comboSourceId: UUID
    comboGroupId: UUID

class ItemsModel(BaseModel):
    type: str
    amount: int
    productSizeId: UUID
    comboInformation: ComboInformationModel
    comment: str
    
class GuestsModel(BaseModel):
    count: int

class CustomerModel(BaseModel):
    id : UUID
    name: str
    surname: str
    comment: str
    birthdate: datetime # ПОФИКСИТЬ ПРИ ТЕСТАХ
    email: str
    shouldReceivePromoActionsInfo: bool
    shouldReceiveOrderStatusNotifications: bool
    #gender: ???????????????????????????????????????????????????
    type: str
    

class TableIdsModel(BaseModel):
    id : UUID


class CombosModel(BaseModel):
    id: UUID
    name: str
    amount: int
    price: int
    sourceId: UUID
    programId: UUID

class PaymentAdditionalDataModel(BaseModel):
    type: str

class PaymentsModel(BaseModel):
    paymentTypeKind: str
    sum: int
    paymentTypeId: UUID
    isProcessedExternally: bool
    paymentAdditionalData: PaymentAdditionalDataModel
    isFiscalizedExternally: bool


class TipsModel(BaseModel):
    paymentTypeKind: str
    tipsTypeId: UUID
    sum: int
    paymentTypeId: UUID
    isProcessedExternally: bool
    paymentAdditionalData: PaymentAdditionalDataModel
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

 
class Order(BaseModel):
    id : UUID
    externalNumber: str
    tableIds: List[TableIdsModel]
    customer: CustomerModel
    phone: str
    guests: GuestsModel
    tabName: str
    items: List[ItemsModel]
    combos: List[CombosModel]
    payments: List[PaymentsModel]
    tips: List[TipsModel]
    sourceKey: str
    discountsInfo: DiscountsInfoModel
    iikoCard5Info: IikoCard5InfoModel
    orderTypeId: UUID
    


class createOrderSettingsModel(BaseModel):
    transportToFrontTimeout: int

class OrderCreate(BaseModel):
    organizationId: UUID
    terminalGroupId: UUID
    order: Order
    createOrderSettings: createOrderSettingsModel
    
class ErrorInfoModel(BaseModel):
    code: str
    
class OrderInfoModel(BaseModel):
    id: UUID
    posId: UUID
    externalNumber: str
    organizationId: UUID
    timestamp: int
    creationStatus: str
    errorInfo: ErrorInfoModel
    #order:
    
    
class OrderResponse(BaseModel):
    correlationId: UUID
    orderInfo: OrderInfoModel