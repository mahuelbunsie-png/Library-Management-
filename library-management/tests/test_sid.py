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

def test_add_and_list_books(client):

    # Add two different books
    frst = add_book(client)
    scnd = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    assert frst["id"] != scnd["id"]

    response = client.get("/books")
    assert response.status_code == 200

    books = {}

    # Organise returned books by ID.

    for book in response.get_json():
        books[book["id"]] = book

    assert len(books) == 2
    assert books[frst["id"]] == {
        "id": frst["id"],
        "title": "Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780441172719",
        "total_copies": 2,
        "available_copies": 2
    }
    assert books[scnd["id"]]["title"] == "Dune"
    assert books[scnd["id"]]["available_copies"] == 1


def test_get_one_book(client):
    frst = add_book(client)
    scnd = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.get(f"/books/{scnd['id']}")

    assert response.status_code == 200
    assert response.get_json() == scnd
    assert response.get_json()["id"] != frst["id"]


def test_search_by_title(client):
    exptd = add_book(client)
    add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.get("/books", query_string={"search": "gAtSbY"})

    assert response.status_code == 200
    assert response.get_json() == [exptd]


def test_search_by_author(client):
    exptd = add_book(client)
    add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.get("/books", query_string={"search": "FITZGERALD"})

    assert response.status_code == 200
    assert response.get_json() == [exptd]


def test_search_no_match(client):
    add_book(client)

    response = client.get("/books", query_string={"search": "NoSuchBook"})

    assert response.status_code == 200
    assert response.get_json() == []
    assert len(client.get("/books").get_json()) == 1


def test_get_missing_book(client):
    exstng = add_book(client)

    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [exstng]


def test_update_book(client):
    book = add_book(client)

    response = client.put(f"/books/{book['id']}", json={
        "title": "The Great Gatsby",
        "author": "Fitzgerald"
    })

    assert response.status_code == 200

    exptd = book.copy()
    exptd["title"] = "The Great Gatsby"
    exptd["author"] = "Fitzgerald"

    assert response.get_json() == exptd

    saved = client.get(f"/books/{book['id']}")
    assert saved.status_code == 200
    assert saved.get_json() == exptd

    search = client.get("/books", query_string={"search": "Fitzgerald"})
    assert search.status_code == 200
    assert search.get_json() == [exptd]


def test_update_missing_book(client):
    book = add_book(client)

    response = client.put("/books/999", json={"title": "Changed"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [book]


def test_delete_book(client):
    frst = add_book(client)
    scnd = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    response = client.delete(f"/books/{frst['id']}")

    assert response.status_code == 204
    assert response.data == b""

    msng = client.get(f"/books/{frst['id']}")
    assert msng.status_code == 404
    assert msng.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [scnd]
    assert client.get(f"/books/{scnd['id']}").get_json() == scnd


def test_delete_book_twice(client):
    frst = add_book(client)
    scnd = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)

    assert client.delete(f"/books/{frst['id']}").status_code == 204
    response = client.delete(f"/books/{frst['id']}")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}
    assert client.get("/books").get_json() == [scnd]


def add_member(client, name="Sid", email="sid@example.com"):
    response = client.post("/members", json={"name": name, "email": email})
    assert response.status_code == 201
    return response.get_json()


@pytest.fixture
def borrowed_book(client):
    book = add_book(client, copies=1)
    brwr = add_member(client)
    wtng = add_member(client, "Alex", "alex@example.com")

    response = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": brwr["id"]
    })

    assert response.status_code == 201
    return book, brwr, wtng, response.get_json()


def test_reserve_borrowed_book(client, borrowed_book):
    book, brwr, wtng, loan = borrowed_book
    assert client.get(
        f"/books/{book['id']}"
    ).get_json()["available_copies"] == 0

    response = client.post("/reservations", json={
        "book_id": book["id"],
        "member_id": wtng["id"]
    })

    assert response.status_code == 201
    resrv = response.get_json()
    assert resrv["book_id"] == book["id"]
    assert resrv["member_id"] == wtng["id"]
    assert resrv["fulfilled"] is False
    assert resrv["reservation_date"]
    assert client.get("/reservations").get_json() == [resrv]

    # Placing a reservation should not change the available copies
    assert client.get(
        f"/books/{book['id']}"
    ).get_json()["available_copies"] == 0


def test_filter_reservations_by_book(client):
    frst_book = add_book(client)
    scnd_book = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)
    frst_mem = add_member(client)
    scnd_mem = add_member(client, "Alex", "alex@example.com")

    # Pair different book and member IDs to check the correct filter is used.
    response = client.post("/reservations", json={
        "book_id": frst_book["id"],
        "member_id": scnd_mem["id"]
    })
    assert response.status_code == 201
    frst_resrv = response.get_json()

    response = client.post("/reservations", json={
        "book_id": scnd_book["id"],
        "member_id": frst_mem["id"]
    })
    assert response.status_code == 201
    scnd_resrv = response.get_json()

    response = client.get("/reservations", query_string={
        "book_id": frst_book["id"]
    })

    assert response.status_code == 200
    assert response.get_json() == [frst_resrv]

    saved = client.get("/reservations")
    assert saved.get_json() == [frst_resrv, scnd_resrv]


def test_filter_reservations_by_member(client):
    frst_book = add_book(client)
    scnd_book = add_book(client, "Dune", "Frank Herbert", "9780441013593", 1)
    frst_mem = add_member(client)
    scnd_mem = add_member(client, "Alex", "alex@example.com")

    # Pair different book and member IDs to check the correct filter is used.
    response = client.post("/reservations", json={
        "book_id": frst_book["id"],
        "member_id": scnd_mem["id"]
    })
    assert response.status_code == 201
    frst_resrv = response.get_json()

    response = client.post("/reservations", json={
        "book_id": scnd_book["id"],
        "member_id": frst_mem["id"]
    })
    assert response.status_code == 201
    scnd_resrv = response.get_json()

    response = client.get("/reservations", query_string={
        "member_id": frst_mem["id"]
    })

    assert response.status_code == 200
    assert response.get_json() == [scnd_resrv]

    saved = client.get("/reservations")
    assert saved.get_json() == [frst_resrv, scnd_resrv]


def test_reserve_missing_book(client):
    book = add_book(client)
    mem = add_member(client)

    response = client.post("/reservations", json={
        "book_id": 999,
        "member_id": mem["id"]
    })

    assert response.status_code == 404
    assert response.get_json() == {"error": "Book not found"}

    saved = client.get("/reservations")
    assert saved.get_json() == []

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json() == book


def test_reserve_missing_member(client):
    book = add_book(client)
    add_member(client)

    response = client.post("/reservations", json={
        "book_id": book["id"],
        "member_id": 999
    })

    assert response.status_code == 404
    assert response.get_json() == {"error": "Member not found"}

    saved = client.get("/reservations")
    assert saved.get_json() == []

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json() == book


# Run the same test with three due-date cases
# -2: due in two days, so no fine
#  0: due today, so no fine
#  3: three days late, so 3 × $0.25 = $0.75
# These amounts use the app's existing daily rate

@pytest.mark.parametrize("days_ovrdue,exptd", [
    (-2, 0.0),
    (0, 0.0),
    (3, 0.75)
])
def test_active_loan_fine(
        client, borrowed_book, days_ovrdue, exptd):

    from datetime import date, timedelta
    from app import store

    book, brwr, wtng, loan = borrowed_book

    # Set the loan dates directly so we can test fines without waiting for days
    recrd = store.loans[loan["id"]]
    recrd.loan_date = date.today() - timedelta(days=20)
    recrd.due_date = date.today() - timedelta(days=days_ovrdue)

    response = client.get(f"/loans/{loan['id']}/fine")

    assert response.status_code == 200
    assert response.get_json() == {
        "loan_id": loan["id"],
        "fine_amount": exptd
    }
    assert recrd.return_date is None


def test_returned_loan_fine(client, borrowed_book):
    from datetime import date, timedelta
    from app import store

    book, brwr, wtng, loan = borrowed_book
    recrd = store.loans[loan["id"]]
    recrd.loan_date = date.today() - timedelta(days=19)
    recrd.due_date = date.today() - timedelta(days=5)
    recrd.return_date = date.today() - timedelta(days=3)

    response = client.get(f"/loans/{loan['id']}/fine")

    assert response.status_code == 200
    # Returned two days late, using the application's existing daily rate.
    assert response.get_json() == {
        "loan_id": loan["id"],
        "fine_amount": 0.50
    }

def test_fine_missing_loan(client):
    response = client.get("/loans/999/fine")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Loan not found"}
    assert client.get("/loans").get_json() == []


def test_rejected_checkout_keeps_records(client, borrowed_book):
    book, brwr, wtng, loan = borrowed_book

    saved_book = client.get(f"/books/{book['id']}").get_json()
    saved_loans = client.get("/loans").get_json()

    response = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": wtng["id"]
    })

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "No book copies available in the current moment"
    }
    assert client.get(f"/books/{book['id']}").get_json() == saved_book
    assert client.get("/loans").get_json() == saved_loans


def test_checkout_last_copy(client):
    book = add_book(client, copies=1)
    mem = add_member(client)

    response = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": mem["id"]
    })

    assert response.status_code == 201
    loan = response.get_json()
    assert loan["book_id"] == book["id"]
    assert loan["member_id"] == mem["id"]
    assert loan["return_date"] is None
    assert client.get("/loans").get_json() == [loan]

    exptd = book.copy()
    exptd["available_copies"] = 0
    assert client.get(f"/books/{book['id']}").get_json() == exptd

































