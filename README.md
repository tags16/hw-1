#### HW-1
###### Требования
```
Python >= 3.8
python-venv >= 3.8
PostgreSQL >= 13
```

###### Сруктура проекта
- `main.py` - основной файл программы
- `dbase.py` - взаимодействие с БД 
- `mbase.py` - валидация данных
- `.env` - базовые параметры проекта

###### Файл конфигурации `.env`
```
# Настройки подключения к БД
DB_USER = "tags16"
DB_PASSWORD = "**********"
DB_HOST = "127.0.0.1"
DB_NAME = "postgres"
```

###### Установка и запуск `HW-1`
1. Выполнить для скачивания проекта: `gh repo clone tags16/hw-1`
2. Создать окружение: `python -m venv venv`
3. Активировать окружение: `source venv/bin/activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Запустить проект `uvicorn main:app --reload`
- Для остановки программы нажать: `ctrl + c`
- Деактивировать окружение: `deactivate`

###### Примечание
После запуска программы создаются 3 таблицы:
- `items` - Список товаров
- `stores` - Список магазинов
- `sales` - Список покупок в магазинах

Таблицы `items` и `stores` наполняются тестовыми данными