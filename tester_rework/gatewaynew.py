#imports
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from routers import DBO, ABS, SM
from models import User
from database import SessionLocal
from authentication.hash_pass import get_password_hash
from authentication.token_creation import create_access_token, decode_token
from authentication.authentication_users import authenticate_user
from datetime import timedelta
import uvicorn
'''Это класс, предоставляемый библиотекой FastAPI. Он упрощает работу с аутентификацией пользователей 
с помощью OAuth 2.0, в частности, с использованием токенов доступа, которые получаются
 посредством предоставления учетных данных пользователя (имени пользователя и пароля).
Данный класс отвечает за извлечение токена из заголовка авторизации HTTP.'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
async def get_db(): #Сессия
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
#Получение модели и подвязка ручек для API
app = FastAPI()
app.include_router(DBO.router)
app.include_router(ABS.router)
app.include_router(SM.router)
'''декоратор, который указывает, что функция register_user 
будет обрабатывать POST-запросы по эндпоинту /register/. 
Это позволяет клиентам отправлять данные для регистрации нового пользователя.'''
@app.post("/register/") 
async def register_user(username: str, email: str, password: str, db: AsyncSession = Depends(get_db)):
    '''username, email и password: строки, которые должны быть переданы при вызове функции. 
    Это данные, необходимые для создания нового пользователя.
     AsyncSession используется зависимость для получения асинхронной сессии базы данных. Функция get_db возвращает 
     объект сессии, который будет использоваться для взаимодействия с базой данных.'''
    query = select(User).filter(User.username == username)
    '''Выполнение запроса к базе данных с использованием асинхронного метода execute. 
    Это позволяет не блокировать выполнение других операций, пока ожидается ответ от базы данных.'''
    result = await db.execute(query)
    '''Получение первого результата из результата запроса. Метод scalars() возвращает только значимые значения, а 
    first() берёт первый элемент из результата. Если пользователь с 
    таким именем существует, эта переменная будет содержать его объект, иначе будет None.'''
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Existing")
    #хеширование пароля с использованием функции get_password_hash.
    hashed_password = await get_password_hash(password)
    new_user = User(username=username, email=email, password_hashed=hashed_password)
    db.add(new_user)
    # Асинхронное подтверждение изменений в базе данных, что сохранит нового пользователя.
    await db.commit()
    await db.refresh(new_user)
    return {"msg": "Success"}
'''декоратор, который указывает, что функция login будет обрабатывать POST-запросы к маршруту /token.
 Этот маршрут используется для получения токена доступа пользователя после аутентификации.'''
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    ''' объект, который автоматически обрабатывает данные формы аутентификации (имя пользователя и пароль) 
    с использованием схемы OAuth2. Данные передаются в таком формате, ч
    то FastAPI может их парсить без дополнительного кода.'''
    user = await authenticate_user(db, form_data.username, form_data.password)
    '''Асинхронный вызов функции authenticate_user, которая проверяет учетные данные 
    в базе данных. Если аутентификация успешна, функция возвращает объект пользователя; если нет — None.'''
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль", headers={"WWW-Authenticate": "Bearer"}, )
    ''' Если аутентификация прошла успешно, вызывается асинхронная функция create_access_token, которая создает JWT (JSON Web Token) с данными (payload). 
    в качестве данных передается {"sub": user.username},
    где "sub" обозначает "субъект". Параметр expires_delta=timedelta(minutes=30) задает время жизни токена.'''
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
    '''Bearer-токен используется для идентификации пользователя и предоставления доступа к его
    личным данным или другим защищенным ресурсам'''
'''Это декоратор FastAPI, который указывает, что функция protected_route будет 
обрабатывать GET-запросы к маршруту /protected/. Этот маршрут является защищенным и требует авторизации токеном.'''
@app.get("/protected/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    '''Определение асинхронной функции protected_route. Эта функция принимает один параметр, token, который автоматически передается с 
    помощью механизма зависимостей (Depends). Здесь используется oauth2_scheme, который мы определяли ранее, для извлечения токена авторизации из заголовка запроса.'''
    payload = await decode_token(token)
    ''' Вызов асинхронной функции decode_token, которая принимает токен и декодирует его, 
    возвращая содержимое токена (payload). Это важно для проверки действительности токена и получения информации о пользователе.'''
    if payload is None: raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")
    return {"msg": f"Добро пожаловать!"}
''' Это еще один декоратор FastAPI, который указывает на корневой маршрут /. Функция read_root будет обрабатывать GET-запросы по этому маршруту.'''
@app.get("/")
def read_root(): return {"message": "Welcome to the club buddy!"}
if __name__ == "__main__": uvicorn.run("gatewaynew:app", reload=True)
#infinite journey
