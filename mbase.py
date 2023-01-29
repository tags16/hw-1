from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float


class Store(BaseModel):
    id: int
    name: str


class SaleIn(BaseModel):
    item_id: int
    store_id: int


class StoreTop(BaseModel):
    store_id: int
    name: str
    sum_1: float


class SaleTop(BaseModel):
    item_id: int
    name: str
    count_1: int