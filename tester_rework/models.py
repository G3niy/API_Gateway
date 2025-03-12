from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
from database import Base
from datetime import datetime 
'''Модель User хранит информацию о пользователях.
Модель Document позволяет хранить информацию о загруженных документах.
- Модель Contract предназначена для хранения информации о контрактах.
- Модель Сontract_Document связывает контракты и документы, позволяя установить взаимосвязь между ними.'''
class User(Base): #Этот класс будет представлять таблицу users в базе данных.
    #literally database of users
    __tablename__ = "users"
    #fields
    id = Column(Integer, primary_key = True) #classics primary key users identify
    username = Column(String, nullable = False)
    email = Column(String, nullable = False)
    password_hashed = Column(String)
    '''hashed password for security - the best way to private users'''
class Document(Base):  #Этот класс будет представлять таблицу documents в базе данных.
    __tablename__ = 'documents'
    doc_id = Column(Integer, primary_key=True, autoincrement=True)  
    file_name = Column(String, nullable=False)  
    file_type = Column(String, nullable=False)  
    upload_date = Column(DateTime, default=datetime.utcnow)
    #поле типа DateTime, которое по умолчанию устанавливается на текущее время при загрузке документа с помощью функции datetime.utcnow().
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    file_data = Column(LargeBinary, nullable=False)
class Contract(Base): #Этот класс будет представлять таблицу contracts в базе данных.
    __tablename__ = 'contract'
    con_id = Column(Integer, primary_key=True, autoincrement=True)
    con_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    #Поле, представляющее дату создания контракта, устанавливаемое по умолчанию на текущее время.
'''linked docs'''
class Сontract_Documentt(Base): #Этот класс будет представлять таблицу linked contracts в базе данных.
    __tablename__ = "contract_document"
    con_doc_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contract.con_id"), nullable = False)
    #Поле, которое ссылается на con_id из таблицы contract, представляющее идентификатор контракта. Это поле обязательно.
    document_id = Column(Integer, ForeignKey("documents.doc_id"), nullable = False)
    date_bind = Column(DateTime, default=datetime.utcnow)