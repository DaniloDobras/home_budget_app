from datetime import datetime

from app.db import models
from app.tests.conftest import TestingSessionLocal


def login_and_get_token(client):
    client.post("/auth/register", json={
        "username": "test_user",
        "password": "test_pass"
    })
    response = client.post("/auth/token", json={
        "username": "test_user",
        "password": "test_pass"
    })
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def create_category_and_get_id(client, token, name="food"):
    response = client.post(
        "/categories/",
        json={"name": name},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    return response.json()["id"]


def get_user_balance_from_db(username: str) -> float:
    with TestingSessionLocal() as db:
        user = db.query(models.User).filter_by(username=username).first()
        return user.balance


def create_bill_and_get_id(
        client,
        token,
        category_id,
        amount=100.0,
        description="Groceries"
):
    response = client.post(
        "/expenses/",
        json={
            "description": description,
            "amount": amount,
            "date": datetime.utcnow().isoformat(),
            "category_id": category_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    return response.json()["id"], response.json()
