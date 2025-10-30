from pydantic import BaseModel
from typing import List, Optional


class FillInventoryRequest(BaseModel):
    product_id: str
    store_id: str
    quantity: int
    user_name: str


class InventoryPayload(BaseModel):
    productId: str
    remainQuantity: int
    stockedInQuantity: int
    storeId: str


class StoreInventory(BaseModel):
    storeId: str
    remainQuantity: int
    stockedInQuantity: int


class InventoryData(BaseModel):
    productId: str
    stores: List[StoreInventory]


class InventoryApiResponse(BaseModel):
    status: str
    code: int
    message: str
    data: InventoryData


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None


class AddProductRequest(BaseModel):
    product_id: str
    product_name: str
    user_name: str


class AddStoreRequest(BaseModel):
    store_id: str
    store_name: str
    user_name: str
