import pytest
from httpx import AsyncClient, ASGITransport
from gatewaynew import app
import httpx

@pytest.fixture(scope="module")
def global_header():
    token_in_header = {"Authorization": ""}
    return token_in_header


@pytest.fixture(scope="module")
def global_fields():
    connect_fields = {"contract_id": "", "document_id": "" }
    return connect_fields
@pytest.mark.asyncio
async def test_token_creation(global_header):
    data = { "username": "admin", "password": "admin", }
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/token", data=data)
        response_json = response.json()
        token = response_json["access_token"]
        assert response.status_code == 200
        global_header["Authorization"] = f"Bearer {token}"
@pytest.mark.asyncio
async def test_downloading_files(global_header, global_fields):
    test_file = ("test_file.txt", b"test content")
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post( "/api/v1/DBO/upload/", files={"file": test_file}, headers=global_header )
        response_json = response.json()
@pytest.mark.asyncio  
async def test_token_get_doc(global_header):  
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:  
        response = await client.get("/api/v1/ABS/client_documents/", headers=global_header)
        response_json = response.json()  
        assert "contract_list" in response_json  
        assert isinstance(response_json["contract_list"], list)
@pytest.mark.asyncio
async def test_contract_writing(global_fields, global_header):
    data = { "name": "Оборот 2024", "desc": "Финансы за 2024", }
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post( "/api/v1/SM/create_contract", params=data, headers=global_header )
        responce_json = response.json()
        global_fields["contract_id"] = responce_json["con_id"]
@pytest.mark.asyncio
async def test_async_writing(global_fields, global_header):
    data = { "name": "default", "desc": "default", }
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post( "/api/v1/SM/create_contract", params=data, headers=global_header )
        responce_json = response.json()
        global_fields["contract_id"] = responce_json["con_id"]