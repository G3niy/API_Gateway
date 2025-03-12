from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile, Depends
from fastapi.security import OAuth2PasswordBearer
from models import Document, User
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from auth.jwt_token import decode_token
router = APIRouter( prefix="/api/v1/DBO", tags=["DBO"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
async def get_db():
    async with SessionLocal() as db:
        try: yield db  
        finally: await db.close()
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    #payload = await decode_token(token)
    #if payload is None: raise HTTPException(status_code=401, detail="Неверный токен или срок действия истёк")
    #if payload["sub"] is None: raise HTTPException(status_code=401, detail="Пользователь не найден в токене")
    #id_user = await db.execute(select(User).filter(User.username == payload["sub"]))
    id_user = 1
    file_content = await file.read()
    db_document = Document( file_name=file.filename, file_type=file.content_type, file_data=file_content, user_id = 1)
    db.add(db_document)
    await db.commit()
    await db.refresh(db_document)
    return { "doc_id": db_document.doc_id, "file_name": db_document.file_name, "file_type": db_document.file_type, "upload_date": db_document.upload_date}
@router.get("/documents/{doc_id}")  
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).filter(Document.doc_id == doc_id))
    document = result.scalars().first()
    if document is None: raise HTTPException(status_code=404, detail="Document not found")
    return { "doc_id": document.doc_id, "file_name": document.file_name, "file_type": document.file_type, "upload_date": document.upload_date}