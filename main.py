from typing import List
from fastapi import FastAPI
import dbase as db # Подключение к БД
import mbase as m # Модели данных

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()

# Получение списка товаров
@app.get("/items/", response_model=List[m.Item])
async def read_items():
    query = db.items.select()
    return await db.database.fetch_all(query)

# Получение списка магазинов
@app.get("/stores/", response_model=List[m.Store])
async def read_stores():
    query = db.stores.select()
    return await db.database.fetch_all(query)

# Добавить информацию о покупке
@app.post("/sale/", response_model=m.SaleIn)
async def create_items(sale: m.SaleIn):
    query = db.sales.insert().values(item_id=sale.item_id, store_id=sale.store_id)
    last_record_id = await db.database.execute(query)
    return {**sale.dict(), 'id': last_record_id}

# Топ 10 самых доходных магазинов за месяц
@app.get("/top-stores/", response_model=List[m.StoreTop])
async def get_top_stores():
    return await db.database.fetch_all(db.storeTop)

# Топ 10 самых продаваемых товаров 
@app.get("/top-sales/", response_model=List[m.SaleTop])
async def get_top_sales():
    return await db.database.fetch_all(db.saleTop)