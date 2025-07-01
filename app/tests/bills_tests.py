from datetime import datetime
from app.tests.test_utils import (login_and_get_token,
                                  create_category_and_get_id,
                                  create_bill_and_get_id,
                                  get_user_balance_from_db)


def test_create_bill(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)
    response = test_client.post(
        "/bills/",
        json={
            "description": "Grocery shopping",
            "amount": 200.0,
            "date": datetime.utcnow().isoformat(),
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Grocery shopping"
    assert data["amount"] == 200.0
    assert data["category_id"] == category_id


def test_get_all_bills(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)
    create_bill_and_get_id(test_client, token, category_id)

    response = test_client.get(
        "/bills/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_bill_by_id(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)
    bill_id, _ = create_bill_and_get_id(test_client, token, category_id)

    response = test_client.get(
        f"/bills/{bill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == bill_id


def test_update_bill(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)
    bill_id, original = create_bill_and_get_id(
        test_client,
        token,
        category_id,
        amount=150
    )

    response = test_client.put(
        f"/bills/{bill_id}",
        json={
            "description": "Updated expense",
            "amount": 50.0,
            "date": datetime.utcnow().isoformat(),
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated expense"
    assert data["amount"] == 50.0


def test_delete_bill(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)
    bill_id, _ = create_bill_and_get_id(test_client, token, category_id)

    response = test_client.delete(
        f"/bills/{bill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    response = test_client.get(
        f"/bills/{bill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_balance_after_adding_bill(test_client):
    token = login_and_get_token(test_client)
    initial_balance = get_user_balance_from_db("test_user")
    category_id = create_category_and_get_id(test_client, token)

    amount = 100.0
    create_bill_and_get_id(test_client, token, category_id, amount=amount)

    updated_balance = get_user_balance_from_db("test_user")
    assert updated_balance == initial_balance - amount


def test_balance_after_deleting_bill(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)

    amount = 150.0
    initial_balance = get_user_balance_from_db("test_user")
    bill_id, _ = create_bill_and_get_id(
        test_client,
        token,
        category_id,
        amount=amount
    )

    balance_after_creation = get_user_balance_from_db("test_user")
    assert balance_after_creation == initial_balance - amount

    test_client.delete(
        f"/bills/{bill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    final_balance = get_user_balance_from_db("test_user")
    assert final_balance == initial_balance


def test_balance_after_updating_bill(test_client):
    token = login_and_get_token(test_client)
    category_id = create_category_and_get_id(test_client, token)

    original_amount = 200.0
    new_amount = 50.0
    bill_id, _ = create_bill_and_get_id(
        test_client,
        token,
        category_id,
        amount=original_amount
    )

    balance_after_creation = get_user_balance_from_db("test_user")
    test_client.put(
        f"/bills/{bill_id}",
        json={
            "description": "Updated to cheaper expense",
            "amount": new_amount,
            "date": datetime.utcnow().isoformat(),
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    final_balance = get_user_balance_from_db("test_user")
    expected_diff = original_amount - new_amount
    assert final_balance == balance_after_creation + expected_diff
