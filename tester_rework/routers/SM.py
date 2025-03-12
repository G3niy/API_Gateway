from sqlalchemy.future import select
from fastapi import FastAPI, APIRouter, HTTPException,  Depends
from models import Document, Contract, Сontract_Documentt
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter( prefix="/api/v1/SM", tags=["SM"])
async def get_db():
    async with SessionLocal() as db:
        try: yield db  
        finally: await db.close()
@router.post("/create_contract")
async def create_contract(name: str, desc: str, db: AsyncSession = Depends(get_db)):
    new_contract = Contract(con_name=name, description=desc)
    db.add(new_contract)
    await db.commit()
    await db.refresh(new_contract)
    return new_contract
@router.get("/get_contract/{con_id}")
async def read_contract(con_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).filter(Contract.con_id == con_id)) 
    contract = result.scalars().first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")  
    return { "con_id": contract.con_id, "con_name": contract.con_name, "description": contract.description, "create_date": contract.create_date}
@router.get("/get_all_contract")
async def read_all_contract(db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Contract))
    contracts = query.scalars().all()
    if contracts is None:  
        raise HTTPException(status_code=404, detail="Contract not found") 
    return {"contract_list": contracts}
@router.delete("/delete_contract")
async def delete_contract(con_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).filter(Contract.con_id == con_id))  
    contract = result.scalars().first()  
    if contract is None: raise HTTPException(status_code=404, detail="Contract not found")  
    await db.delete(contract)
    await db.commit()
    return {"detail": "Contract deleted successfully"}
@router.post("/connect_contract_document")
async def connect_doc_contract(con_id: int, doc_id: int, db: AsyncSession = Depends(get_db)):
    new_connect = Сontract_Documentt(contract_id=con_id, document_id=doc_id)
    db.add(new_connect)
    await db.commit()
    await db.refresh(new_connect)
    return new_connect
@router.get("/read_contract_document")
async def read_doc_contract(con_doc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Сontract_Documentt).filter(Сontract_Documentt.con_doc_id == con_doc_id))  
    contract_document = result.scalars().first()  
    result = await db.execute(select(Document).filter(Document.doc_id == contract_document.document_id))
    document = result.scalars().first()
    result = await db.execute(select(Contract).filter(Contract.con_id == contract_document.contract_id))
    contract = result.scalars().first()
    if contract_document is None: raise HTTPException(status_code=404, detail="Contract not found")  
    return {"Документ": f"Привязан к контракту c id {contract_document.contract_id}", "file_name": document.file_name, "file_type": document.file_type, "Контракт": f"Привязан к документу c id {contract_document.document_id}", "con_name": contract.con_name, "description": contract.description, "Дата привязки": contract_document.date_bind}