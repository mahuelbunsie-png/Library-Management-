from unittest.mock import patch

from test_mahuel import add_book, add_member


def test_checkout_notification_success_stub(client, monkeypatch):
    # A stub forces the notification service to report success.
    monkeypatch.setattr(
        "app.routes.loans.send_notification",
        lambda recipient, subject, message: True
    )

    book = add_book(client)
    member = add_member(client)

    response = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })

    # Verify application behavior and saved state.
    assert response.status_code == 201

    loan = response.get_json()
    assert loan["book_id"] == book["id"]
    assert loan["member_id"] == member["id"]

    saved_loans = client.get("/loans").get_json()
    assert saved_loans == [loan]

    saved_book = client.get(f"/books/{book['id']}").get_json()
    assert saved_book["available_copies"] == book["available_copies"] - 1

def test_checkout_notification_success_mock(client):
    book = add_book(client)
    member = add_member(client)

    with patch(
        "app.routes.loans.send_notification",
        return_value=True
    ) as mock_send:

        response = client.post("/loans", json={
            "book_id": book["id"],
            "member_id": member["id"]
        })

    # Verify the checkout succeeded.
    assert response.status_code == 201
    loan = response.get_json()

    assert loan["book_id"] == book["id"]
    assert loan["member_id"] == member["id"]

    # Verify the notification recipient, subject, and message.
    mock_send.assert_called_once_with(
        member["email"],
        "[Library Management System] Book Checkout Confirmation",
        f"Your checkout for book ID {book['id']} was successful. "
        f"Your loan ID is {loan['id']}, and the due date is {loan['due_date']}."
    )

    # Verify the application saved the loan correctly.
    assert client.get("/loans").get_json() == [loan]
    assert client.get(
        f"/books/{book['id']}"
    ).get_json()["available_copies"] == book["available_copies"] - 1

def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Library Management System" in response.data

def test_books_page(client):
    book = add_book(client)

    response = client.get("/ui/books")

    assert response.status_code == 200
    assert book["title"].encode() in response.data

def test_delete_book_page(client):
    book = add_book(client)

    response = client.post(f"/ui/books/{book['id']}/delete")

    assert response.status_code in (302, 303)
    assert client.get(f"/books/{book['id']}").status_code == 404

def test_renew_returned_loan(client):
    book = add_book(client)
    member = add_member(client)

    checkout = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })
    assert checkout.status_code == 201

    loan = checkout.get_json()

    returned = client.put(f"/loans/{loan['id']}/return")
    assert returned.status_code == 200

    response = client.put(f"/loans/{loan['id']}/renew")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Loan already returned"}

    saved_loan = client.get("/loans").get_json()[0]
    assert saved_loan["due_date"] == loan["due_date"]
    assert saved_loan["return_date"] is not None

def test_delete_missing_book_page(client):
    response = client.post("/ui/books/9999/delete")

    assert response.status_code in (302, 303)

    # The missing book should not be created.
    assert client.get("/books/9999").status_code == 404

    # The library should still have no books.
    assert client.get("/books").get_json() == []

def test_add_book_through_web_page(client):
    response = client.post("/ui/books", data={
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "total_copies": "3"
    })

    # The form should redirect to the books page.
    assert response.status_code in (302, 303)

    # Verify the book was actually saved.
    books = client.get("/books").get_json()

    assert len(books) == 1
    assert books[0]["title"] == "Clean Code"
    assert books[0]["author"] == "Robert C. Martin"
    assert books[0]["total_copies"] == 3
    assert books[0]["available_copies"] == 3