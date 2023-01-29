import os
import databases
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float, DateTime, insert, select, desc
from sqlalchemy.sql import func
load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

items = Table('items', metadata,
	Column('id', Integer(), primary_key=True, autoincrement=True, comment='id товара'),
	Column('name', String(), unique=True, comment='Наименование товара'),
	Column('price', Float(), nullable=False, comment='Стоимость товара'),
)

stores = Table('stores', metadata,
	Column('id', Integer(), primary_key=True, autoincrement=True, comment='id магазина'),
	Column('name',String(), comment='=Имя магазина')

)

sales = Table('sales', metadata,
	Column('id', Integer(), primary_key=True, autoincrement=True, comment='id продажи'),
	Column('sale_time', DateTime(), server_default=func.now(), nullable=False, comment='Время продажи'),
	Column('item_id', Integer(), ForeignKey(items.c.id), comment='id проданого товара'),
	Column('store_id', Integer(), ForeignKey(stores.c.id), comment='id магазина из которого был продан товар')
)

# Создание таблиц в бд если их нет
metadata.create_all(engine)

# Проверить есть ли тестовые данные, если нет то заполнить
conn = engine.connect()
r = conn.execute(items.select())
if len(r.fetchall()) == 0:
	items_list = [
		{
			"name":"Пила Zubr ZPT-255-1800PL",
			"price": 8935.3
		},
		{
			"name":"Пила STIHL MS 180 35",
			"price": 11869.0
		},
		{
			"name":"Пила Zubr ZPT-210-1600PL",
			"price": 7132.4
		},
		{
			"name":"Пила Zubr ZPT-210-1400L",
			"price": 3969.9
		},
		{
			"name":"Пила Metabo KGS 216 M",
			"price": 15275.7
		},
		{
			"name":"Пила Hammer STL1400",
			"price": 6490.0
		},
		{
			"name":"Пила Makita HS7601",
			"price": 6927.8
		},
		{
			"name":"Пила Bosch PTS 10",
			"price": 25759.8
		},
		{
			"name":"Пила Interskol DP-190/1600M",
			"price": 4605.7
		},
		{
			"name":"Пила Zubr ZPTK-255-1800",
			"price": 9298.3
		},
		{
			"name":"Пила Zubr ZPTK-210-1500",
			"price": 6590.1
		},
		{
			"name":"Пила Hitachi C7SS",
			"price": 4639.8
		},
		{
			"name":"Пила Metabo KGS 305 M",
			"price": 23647.8
		},
		{
			"name":"Пила Bosch EasyCut 12",
			"price": 6039.0
		},
		{
			"name":"Пила Metabo KS 216 M Lasercut",
			"price": 7037.8
		},
		{
			"name":"Пила Bort BHK-185U",
			"price": 2832.5
		},
		{
			"name":"Пила Makita EA3202S40B",
			"price": 9210.3
		},
		{
			"name":"Пила Metabo KGS 254 M",
			"price": 18868.3
		},
		{
			"name":"Пила Husqvarna 450 e",
			"price": 18205.0
		},
		{
			"name":"Пила STATUS CP90U",
			"price": 5144.7
		},
	]
	conn.execute(insert(items), items_list)

# Проверить есть ли тестовые данные, если нет то заполнить
r = conn.execute(stores.select())
if len(r.fetchall()) == 0:
	stores_list = [
		{
			"name":"Пилматериалы"
		},
		{
			"name":"Наш инструмент"
		},
		{
			"name":"Всем пилы"
		},
		{
			"name":"Даешь инструменты"
		}
	]
	conn.execute(insert(stores), stores_list)

# sql для "топ 10 самых доходных магазинов за месяц"
storeTop = select([
	sales.c.store_id,
	stores.c.name,
	func.sum(items.c.price)
]).select_from(
	sales.join(stores).join(items)
).where(func.to_char(sales.c.sale_time, 'Month') == func.to_char(func.now(), 'Month')).group_by(sales.c.store_id, stores.c.name).order_by(desc(func.sum(items.c.price))).limit(10)

# sql для "топ 10 самых продаваемых товаров"
saleTop = select([
	sales.c.item_id,
	items.c.name,
	func.count(sales.c.item_id)
]).select_from(
	sales.join(items)
).group_by(sales.c.item_id, items.c.name).order_by(desc(func.count(sales.c.item_id))).limit(10)