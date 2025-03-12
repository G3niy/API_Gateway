#imports
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
DATABASE_URL = 'postgresql+asyncpg://postgres:1234@localhost/testdb' #url to database
#postgresql+asyncpg://user:pass@localhost/base_name
engine = create_async_engine(DATABASE_URL) # создает асинхронный объект engine, который служит для подключения к базе данных.
'''create_async_engine — это функция из SQLAlchemy, предназначенная для создания асинхронного движка (engine).
Она позволяет выполнять асинхронные операции с базой данных.'''
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession) # создает класс сессии SessionLocal, который будет использоваться для работы с базой данных.
'''функция, которая создает новый класс сессий. Она использует bind=engine для привязки сессии к ранее созданному
 асинхронному движку engine. Это значит, что все операции, выполненные через экземпляры этого класса, 
 будут отправляться на базу данных через этот движок.'''
Base = declarative_base() # создает базовый класс для всех моделей.
#наследование всех классов таблиц моделей.
