import pytest
import pytest_asyncio
from models import FoundItem


@pytest_asyncio.fixture
async def add_item(test_db):
    item = {"name": "TestFoundItem1", "location": "test location"}
    db_item = FoundItem(**item)
    test_db.add(db_item)
    await test_db.commit()
    await test_db.refresh(db_item)
    return db_item


@pytest.mark.asyncio
async def test_get_found_items_empty_db(client):
    response = await client.get("/found_items/")
    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.asyncio
async def test_get_found_items(client, add_item):
    db_item = add_item
    response = await client.get("/found_items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == db_item.name
    assert data[0]["location"] == db_item.location


@pytest.mark.asyncio
async def test_create_found_items(client):
    item_data = {"name": "Зонтик", "location": "возле дома"}
    response = await client.post("/found_items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["location"] == item_data["location"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_found_item_by_id(client, add_item):
    db_item = add_item
    response = await client.get(f"/found_items/{db_item.id}")
    assert response.status_code == 200
    assert response.json()["name"] == db_item.name


@pytest.mark.asyncio
async def test_update_found_items(client, test_db, add_item):
    new_data = {"name": "TestFoundItem2"}
    db_item = add_item
    assert add_item.id == 1
    assert db_item.name != new_data["name"]
    response = await client.put("/found_items/1", json=new_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_data["name"]
    db_item = await test_db.get(FoundItem, 1)
    assert db_item.name == new_data["name"]


@pytest.mark.asyncio
async def test_delete_found_item(client, test_db, add_item):
    db_item = await test_db.get(FoundItem, 1)
    assert db_item is not None
    await client.delete("/found_items/1")
    db_item = await test_db.get(FoundItem, 1)
    assert db_item is None


# negative tests
@pytest.mark.asyncio
async def test_create_found_items_incorrect_data(client):
    """
    Проверяем, что если при создании нового объекта передать недостаточно данных,
    post("/found_items/") завершится с кодом ошибки 422
    После реализации, убрать @pytest.mark.skip
    """
    responce = await client.post("/found_items/")
    assert responce.status_code == 422


@pytest.mark.asyncio
async def test_get_found_item_by_id_404(client):
    response = await client.get(f"/found_items/{1}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_found_item_404(client):
    response = await client.delete("/found_items/1")
    assert response.status_code == 404
