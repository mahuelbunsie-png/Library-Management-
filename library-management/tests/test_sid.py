import pytest


def add_book(client, title="Great Gatsby", author="F. Scott Fitzgerald",
             isbn="9780441172719", copies=2):
    response = client.post("/books", json={
        "title": title,
        "author": author,
        "isbn": isbn,
        "total_copies": copies
    })
    assert response.status_code == 201
    return response.get_json()


def test_created_books_are_saved_and_listed(client):
    first = add_book(client)
    second = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    assert first["id"] != second["id"]

    response = client.get("/books")
    assert response.status_code == 200
    books = {book["id"]: book for book in response.get_json()}

    assert len(books) == 2
    assert books[first["id"]] == {
        "id": first["id"],
        "title": "Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780441172719",
        "total_copies": 2,
        "available_copies": 2
    }
    assert books[second["id"]]["title"] == "Dune"
    assert books[second["id"]]["available_copies"] == 1


def test_get_book_returns_only_requested_record(client):
    first = add_book(client)
    second = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.get(f"/books/{second['id']}")

    assert response.status_code == 200
    assert response.get_json() == second
    assert response.get_json()["id"] != first["id"]


@pytest.mark.parametrize("search", ["gAtSbY", "FITZGERALD"])
def test_search_matches_title_or_author(client, search):
    expected = add_book(client)
    add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.get("/books", query_string={"search": search})

    assert response.status_code == 200
    assert response.get_json() == [expected]


def test_search_with_no_match_returns_empty_list(client):
    add_book(client)

    response = client.get("/books", query_string={"search": "NoSuchBook"})

    assert response.status_code == 200
    assert response.get_json() == []
    assert len(client.get("/books").get_json()) == 1


def test_get_missing_book_returns_error_without_changing_records(client):
    existing = add_book(client)

    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [existing]


def test_update_book_saves_changes_and_preserves_other_fields(client):
    book = add_book(client)

    response = client.put(f"/books/{book['id']}", json={
        "title": "The Great Gatsby",
        "author": "Fitzgerald"
    })

    assert response.status_code == 200
    expected = dict(book, title="The Great Gatsby", author="Fitzgerald")
    assert response.get_json() == expected
    assert client.get(f"/books/{book['id']}").get_json() == expected
    assert client.get(
        "/books", query_string={"search": "Fitzgerald"}
    ).get_json() == [expected]


def test_update_missing_book_leaves_existing_book_unchanged(client):
    book = add_book(client)

    response = client.put("/books/999", json={"title": "Changed"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [book]


def test_delete_book_removes_only_selected_record(client):
    first = add_book(client)
    second = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.delete(f"/books/{first['id']}")

    assert response.status_code == 204
    assert response.data == b""

    missing = client.get(f"/books/{first['id']}")
    assert missing.status_code == 404
    assert missing.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [second]
    assert client.get(f"/books/{second['id']}").get_json() == second


def test_delete_book_twice_returns_error_without_removing_other_books(client):
    first = add_book(client)
    second = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    assert client.delete(f"/books/{first['id']}").status_code == 204
    response = client.delete(f"/books/{first['id']}")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [second]


def add_member(client, name="Sid", email="sid@example.com"):
    response = client.post("/members", json={"name": name, "email": email})
    assert response.status_code == 201
    return response.get_json()


@pytest.fixture
def borrowed_book(client):
    book = add_book(client, copies=1)
    borrower = add_member(client)
    waiting = add_member(client, "Alex", "alex@example.com")

    response = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": borrower["id"]
    })

    assert response.status_code == 201
    return book, borrower, waiting, response.get_json()


def test_reservation_for_borrowed_book_is_saved(client, borrowed_book):
    book, borrower, waiting, loan = borrowed_book
    assert client.get(
        f"/books/{book['id']}"
    ).get_json()["available_copies"] == 0

    response = client.post("/reservations", json={
        "book_id": book["id"],
        "member_id": waiting["id"]
    })

    assert response.status_code == 201
    reservation = response.get_json()
    assert reservation["book_id"] == book["id"]
    assert reservation["member_id"] == waiting["id"]
    assert reservation["fulfilled"] is False
    assert reservation["reservation_date"]
    assert client.get("/reservations").get_json() == [reservation]
    assert client.get(
        f"/books/{book['id']}"
    ).get_json()["available_copies"] == 0


@pytest.mark.parametrize("filter_name", ["book_id", "member_id"])
def test_reservation_filter_returns_only_matches(client, filter_name):
    first_book = add_book(client)
    second_book = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)
    first_member = add_member(client)
    second_member = add_member(client, "Alex", "alex@example.com")
    saved = []

    for book, member in [(first_book, first_member),
                         (second_book, second_member)]:
        response = client.post("/reservations", json={
            "book_id": book["id"],
            "member_id": member["id"]
        })
        assert response.status_code == 201
        saved.append(response.get_json())

    response = client.get("/reservations", query_string={
        filter_name: saved[1][filter_name]
    })

    assert response.status_code == 200
    assert response.get_json() == [saved[1]]
    assert client.get("/reservations").get_json() == saved


@pytest.mark.parametrize("missing", ["book", "member"])
def test_reservation_with_missing_record_is_rejected(client, missing):
    book = add_book(client)
    member = add_member(client)
    payload = {"book_id": book["id"], "member_id": member["id"]}
    payload[f"{missing}_id"] = 999

    response = client.post("/reservations", json=payload)

    assert response.status_code == 404
    assert response.get_json() == {
        "error": f"{missing.capitalize()} not found"
    }
    assert client.get("/reservations").get_json() == []
    assert client.get(f"/books/{book['id']}").get_json() == book


@pytest.mark.parametrize("days_overdue,expected", [
    (-2, 0.0),
    (0, 0.0),
    (3, 0.75)
])
def test_active_loan_fine_before_on_and_after_due_date(
        client, borrowed_book, days_overdue, expected):
    from datetime import date, timedelta
    from app import store

    book, borrower, waiting, loan = borrowed_book
    record = store.loans[loan["id"]]
    record.loan_date = date.today() - timedelta(days=20)
    record.due_date = date.today() - timedelta(days=days_overdue)

    response = client.get(f"/loans/{loan['id']}/fine")

    assert response.status_code == 200
    assert response.get_json() == {
        "loan_id": loan["id"],
        "fine_amount": expected
    }
    assert record.return_date is None


def test_returned_loan_fine_stops_at_return_date(client, borrowed_book):
    from datetime import date, timedelta
    from app import store

    book, borrower, waiting, loan = borrowed_book
    record = store.loans[loan["id"]]
    record.loan_date = date.today() - timedelta(days=19)
    record.due_date = date.today() - timedelta(days=5)
    record.return_date = date.today() - timedelta(days=3)

    response = client.get(f"/loans/{loan['id']}/fine")

    assert response.status_code == 200
    # Returned two days late, using the application's existing daily rate.
    assert response.get_json() == {
        "loan_id": loan["id"],
        "fine_amount": 0.50
    }


def test_fine_for_missing_loan_returns_error(client):
    response = client.get("/loans/999/fine")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Loan not found"}
    assert client.get("/loans").get_json() == []
