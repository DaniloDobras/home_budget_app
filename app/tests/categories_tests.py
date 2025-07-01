def login_and_get_token(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpass"
    })
    response = client.post("/auth/token", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_create_category(test_client):
    token = login_and_get_token(test_client)
    response = test_client.post(
        "/categories",
        json={"name": "food"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "food"


def test_get_all_categories(test_client):
    token = login_and_get_token(test_client)
    response = test_client.get(
        "/categories",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def create_category_and_get_id(client, token, name="food"):
    response = client.post(
        "/categories/",
        json={"name": name},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]


def test_get_category_by_id(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)

    response = test_client.get(
        f"/categories/id/{category_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == category_id


def test_get_category_by_name(test_client):
    token = login_and_get_token(test_client)
    category_name = "food"
    create_category_and_get_id(test_client, token, name=category_name)

    response = test_client.get(
        f"/categories/name/{category_name}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == category_name


def test_update_category(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)

    response = test_client.put(
        f"/categories/{category_id}",
        json={"name": "groceries"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "groceries"


def test_delete_category(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)

    response = test_client.delete(
        f"/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    response = test_client.get(
        f"/categories/id/{category_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
