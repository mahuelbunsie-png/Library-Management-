from app import store


def test_add_member_ui(client):
    response = client.post("/ui/members", data={
        "name": "Siddhant",
        "email": "siddhant@example.com"
    })

    assert response.status_code == 302
    assert len(store.members) == 1

    mem = list(store.members.values())[0]

    assert mem.name == "Siddhant"
    assert mem.email == "siddhant@example.com"

    response = client.get("/ui/members")

    assert response.status_code == 200
    assert b"Siddhant" in response.data

def test_delete_member_ui(client):
    response = client.post("/ui/members", data={
        "name": "Siddhant",
        "email": "siddhant@example.com"
    })

    assert response.status_code == 302
    assert len(store.members) == 1

    mem = list(store.members.values())[0]

    response = client.post(f"/ui/members/{mem.id}/delete")

    assert response.status_code == 302
    assert len(store.members) == 0

def test_add_loan_ui(client):
    book = client.post("/books", json={
        "title": "The Sentence Is Death",
        "author": "Anthony Horowitz",
        "isbn": "9780062676812",
        "total_copies": 1
    }).get_json()

    mem = client.post("/members", json={
        "name": "Siddhant",
        "email": "siddhant@example.com"
    }).get_json()

    response = client.post("/ui/loans", data={
        "book_id": book["id"],
        "member_id": mem["id"]
    })

    assert response.status_code == 302
    assert len(store.loans) == 1

    loan = list(store.loans.values())[0]

    assert loan.book_id == book["id"]
    assert loan.member_id == mem["id"]

    # Check that one copy was borrowed
    assert store.books[book["id"]].available_copies == 0

    response = client.get("/ui/loans")
    assert response.status_code == 200


def test_return_loan_ui(client):
    book = client.post("/books", json={
        "title": "The Sentence Is Death",
        "author": "Anthony Horowitz",
        "isbn": "9780062676812",
        "total_copies": 1
    }).get_json()

    mem = client.post("/members", json={
        "name": "Siddhant",
        "email": "siddhant@example.com"
    }).get_json()

    response = client.post("/ui/loans", data={
        "book_id": book["id"],
        "member_id": mem["id"]
    })

    assert response.status_code == 302
    assert store.books[book["id"]].available_copies == 0

    loan = list(store.loans.values())[0]

    response = client.post(f"/ui/loans/{loan.id}/return")

    assert response.status_code == 302

    # Check that the book was returned
    assert loan.return_date is not None
    assert store.books[book["id"]].available_copies == 1


def test_checkout_notification_failure_stub(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.loans.send_notification",
        lambda recipient, subject, message: False
    )

    book = client.post("/books", json={
        "title": "The Sentence Is Death",
        "author": "Anthony Horowitz",
        "isbn": "9780062676812",
        "total_copies": 1
    }).get_json()

    mem = client.post("/members", json={
        "name": "Siddhant",
        "email": "siddhant@example.com"
    }).get_json()

    resp = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": mem["id"]
    })

    assert resp.status_code == 201
    assert len(store.loans) == 1
    assert store.books[book["id"]].available_copies == 0


def test_checkout_notification_not_called(client):
    from unittest.mock import patch

    mem = client.post("/members", json={
        "name": "Siddhant",
        "email": "siddhant@example.com"
    }).get_json()

    with patch("app.routes.loans.send_notification") as mock_send:
        resp = client.post("/loans", json={
            "book_id": 999,
            "member_id": mem["id"]
        })

    assert resp.status_code == 404
    assert len(store.loans) == 0
    mock_send.assert_not_called()








