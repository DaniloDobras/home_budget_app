from app.tests.test_utils import login_and_get_token, create_category_and_get_id


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
