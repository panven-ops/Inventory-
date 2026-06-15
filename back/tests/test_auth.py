def test_register(client):
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200

def test_register_duplicate(client):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400

def test_login(client):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/login", json={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401
