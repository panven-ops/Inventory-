import pytest

# Helper που κάνει register+login και επιστρέφει token
@pytest.fixture
def auth_client(client):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    res = client.post("/login", json={"username": "testuser", "password": "testpass"})
    token = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

def test_create_item(auth_client):
    response = auth_client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_get_items(auth_client):
    auth_client.post("/items", json={"name": "Item 1"})
    auth_client.post("/items", json={"name": "Item 2"})
    response = auth_client.get("/items?skip=0&limit=10")
    assert response.status_code == 200
    assert response.json()["total"] == 2

def test_pagination(auth_client):
    for i in range(15):
        auth_client.post("/items", json={"name": f"Item {i}"})
    response = auth_client.get("/items?skip=0&limit=10")
    assert len(response.json()["data"]) == 10
    assert response.json()["total"] == 15
    assert response.json()["pages"] == 2

def test_delete_item(auth_client):
    res = auth_client.post("/items", json={"name": "To Delete"})
    print(res.json())
    item_id = res.json()["id"]
    response = auth_client.delete(f"/items/{item_id}")
    assert response.status_code == 200

def test_delete_other_user_item(client):
    # User A
    client.post("/register", json={"username": "userA", "password": "password853"})
    res = client.post("/login", json={"username": "userA", "password": "password853"})
    tokenA = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {tokenA}"})
    item = client.post("/items", json={"name": "User A item"}).json()

    # User B tries to delete item του A
    client.post("/register", json={"username": "userB", "password": "password853"})
    res = client.post("/login", json={"username": "userB", "password": "password853"})
    tokenB = res.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {tokenB}"})
    response = client.delete(f"/items/{item['id']}")
    assert response.status_code == 403
