def add_member(client, name="Mahuel", email="mahuel@example.com"):
    response = client.post("/members", json={
        "name": name,
        "email": email
    })
    assert response.status_code == 201
    return response.get_json()


def test_add_and_list_members(client):
    member_one = add_member(client)
    member_two = add_member(client, "Sid", "sid@example.com")

    assert member_one["id"] != member_two["id"]
    assert member_one["name"] == "Mahuel"
    assert member_one["email"] == "mahuel@example.com"
    assert member_one["membership_date"]
    assert member_two["name"] == "Sid"
    assert member_two["email"] == "sid@example.com"
    assert member_two["membership_date"]

    result = client.get("/members")

    assert result.status_code == 200

    # Organise the returned members by ID
    members_by_id = {}
    for member in result.get_json():
        members_by_id[member["id"]] = member

    assert len(members_by_id) == 2
    assert members_by_id[member_one["id"]] == member_one
    assert members_by_id[member_two["id"]] == member_two


def test_get_one_member(client):
    member_one = add_member(client)
    member_two = add_member(client, "Sid", "sid@example.com")

    result = client.get(f"/members/{member_two['id']}")

    assert result.status_code == 200
    assert result.get_json() == member_two
    assert result.get_json()["id"] != member_one["id"]



def test_update_member(client):
    member = add_member(client)

    result = client.put(f"/members/{member['id']}", json={
        "name": "Mahuel Bunsie"
    })

    assert result.status_code == 200

    expected = member.copy()
    expected["name"] = "Mahuel Bunsie"

    assert result.get_json() == expected

    saved_member = client.get(f"/members/{member['id']}")
    assert saved_member.status_code == 200
    assert saved_member.get_json() == expected

    members = client.get("/members")
    assert members.get_json() == [expected]


def test_get_missing_member(client):
    member = add_member(client)

    result = client.get("/members/999")

    assert result.status_code == 404
    assert result.get_json() == {"error": "Member not found"}
    assert client.get("/members").get_json() == [member]


def test_update_missing_member(client):
    member = add_member(client)

    result = client.put("/members/999", json={"name": "Changed"})

    assert result.status_code == 404
    assert result.get_json() == {"error": "Member not found"}
    assert client.get("/members").get_json() == [member]


def test_delete_member(client):
    member_one = add_member(client)
    member_two = add_member(client, "Sid", "sid@example.com")

    result = client.delete(f"/members/{member_one['id']}")

    assert result.status_code == 204
    assert result.data == b""

    deleted_member = client.get(f"/members/{member_one['id']}")
    assert deleted_member.status_code == 404
    assert deleted_member.get_json() == {"error": "Member not found"}

    assert client.get("/members").get_json() == [member_two]
    assert client.get(
        f"/members/{member_two['id']}"
    ).get_json() == member_two


def test_delete_member_twice(client):
    member_one = add_member(client)
    member_two = add_member(client, "Sid", "sid@example.com")

    result = client.delete(f"/members/{member_one['id']}")
    assert result.status_code == 204

    result = client.delete(f"/members/{member_one['id']}")

    assert result.status_code == 404
    assert result.get_json() == {"error": "Member not found"}
    assert client.get("/members").get_json() == [member_two]




def add_book(client, copies=2):
    response = client.post("/books", json={
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "9780441013593",
        "total_copies": copies
    })
    assert response.status_code == 201
    return response.get_json()


def test_checkout_book(client):
    from datetime import date, timedelta

    book = add_book(client)
    member = add_member(client)

    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })

    assert result.status_code == 201
    loan = result.get_json()

    assert loan["book_id"] == book["id"]
    assert loan["member_id"] == member["id"]
    assert loan["loan_date"] == date.today().isoformat()

    # The starter app uses a 14-day loan period
    expected_due = date.today() + timedelta(days=14)
    assert loan["due_date"] == expected_due.isoformat()
    assert loan["return_date"] is None

    saved_loans = client.get("/loans")
    assert saved_loans.status_code == 200
    assert saved_loans.get_json() == [loan]

    expected_book = book.copy()
    expected_book["available_copies"] = 1

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json() == expected_book


def test_checkout_missing_book(client):
    book = add_book(client)
    member = add_member(client)

    result = client.post("/loans", json={
        "book_id": 999,
        "member_id": member["id"]
    })

    assert result.status_code == 404
    assert result.get_json() == {"error": "Book not found"}
    assert client.get("/loans").get_json() == []
    assert client.get(f"/books/{book['id']}").get_json() == book


def test_checkout_unavailable_book(client):
    book = add_book(client, copies=1)
    member = add_member(client)

    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })
    assert result.status_code == 201
    loan = result.get_json()

    # The only copy is already borrowed
    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })

    assert 400 <= result.status_code < 500
    assert client.get("/loans").get_json() == [loan]

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json()["available_copies"] == 0




def test_return_loan(client):
    from datetime import date

    book = add_book(client)
    member = add_member(client)

    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })
    assert result.status_code == 201
    loan = result.get_json()

    result = client.put(f"/loans/{loan['id']}/return")

    assert result.status_code == 200

    expected = loan.copy()
    expected["return_date"] = date.today().isoformat()

    assert result.get_json() == expected
    assert client.get("/loans").get_json() == [expected]

    # Returning the book restores its available copies.
    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json() == book


def test_return_missing_loan(client):
    book = add_book(client)

    result = client.put("/loans/999/return")

    assert result.status_code == 404
    assert result.get_json() == {"error": "Loan not found"}
    assert client.get("/loans").get_json() == []
    assert client.get(f"/books/{book['id']}").get_json() == book


def test_return_loan_twice(client):
    book = add_book(client)
    member = add_member(client)

    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })
    assert result.status_code == 201
    loan = result.get_json()

    result = client.put(f"/loans/{loan['id']}/return")
    assert result.status_code == 200
    returned_loan = result.get_json()

    result = client.put(f"/loans/{loan['id']}/return")

    assert result.status_code == 400
    assert result.get_json() == {"error": "Loan already returned"}
    assert client.get("/loans").get_json() == [returned_loan]

    # A second return must not increase the available copies again
    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json() == book


def add_loan(client, book, member):
    response = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })
    assert response.status_code == 201
    return response.get_json()


def test_filter_loans_by_book(client):
    book_one = add_book(client)
    book_two = add_book(client)
    member_one = add_member(client)
    member_two = add_member(client, "Sid", "sid@example.com")

    # Cross the book and member IDs to detect use of the wrong field
    loan_one = add_loan(client, book_one, member_two)
    loan_two = add_loan(client, book_two, member_one)

    result = client.get("/loans", query_string={
        "book_id": book_one["id"]
    })

    assert result.status_code == 200
    assert result.get_json() == [loan_one]

    saved_loans = client.get("/loans")
    assert saved_loans.get_json() == [loan_one, loan_two]


def test_filter_loans_by_member(client):
    book_one = add_book(client)
    book_two = add_book(client)
    member_one = add_member(client)
    member_two = add_member(client, "Sid", "sid@example.com")

    # Cross the book and member IDs to detect use of the wrong field
    loan_one = add_loan(client, book_one, member_two)
    loan_two = add_loan(client, book_two, member_one)

    result = client.get("/loans", query_string={
        "member_id": member_one["id"]
    })

    assert result.status_code == 200
    assert result.get_json() == [loan_two]

    saved_loans = client.get("/loans")
    assert saved_loans.get_json() == [loan_one, loan_two]





def test_renew_loan(client):
    from datetime import date, timedelta

    book = add_book(client)
    member = add_member(client)
    loan = add_loan(client, book, member)

    result = client.put(f"/loans/{loan['id']}/renew")

    assert result.status_code == 200

    # Renewal adds 14 days to the existing due date
    old_due = date.fromisoformat(loan["due_date"])
    new_due = old_due + timedelta(days=14)

    expected = loan.copy()
    expected["due_date"] = new_due.isoformat()

    assert result.get_json() == expected
    assert client.get("/loans").get_json() == [expected]

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json()["available_copies"] == 1


def test_renew_with_waiting_member(client):
    book = add_book(client, copies=1)
    borrower = add_member(client)
    waiting_member = add_member(client, "Sid", "sid@example.com")
    loan = add_loan(client, book, borrower)

    result = client.post("/reservations", json={
        "book_id": book["id"],
        "member_id": waiting_member["id"]
    })
    assert result.status_code == 201
    reservation = result.get_json()

    # Another member has a hold, and no copies are available
    result = client.put(f"/loans/{loan['id']}/renew")

    assert 400 <= result.status_code < 500
    assert client.get("/loans").get_json() == [loan]
    assert client.get("/reservations").get_json() == [reservation]

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.get_json()["available_copies"] == 0

def test_delete_missing_member(client):
    member = add_member(client)

    result = client.delete("/members/999")

    assert result.status_code == 404
    assert result.get_json() == {"error": "Member not found"}

    # Deleting a nonexistent member should not affect existing members.
    saved_members = client.get("/members")
    assert saved_members.status_code == 200
    assert saved_members.get_json() == [member]

def test_checkout_missing_member(client):
    book = add_book(client)

    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": 999
    })

    # A loan cannot be created for a nonexistent member.
    assert result.status_code == 404
    assert result.get_json() == {"error": "Member not found"}

    # Failed checkout should not create a loan or change availability.
    assert client.get("/loans").get_json() == []

    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.status_code == 200
    assert saved_book.get_json() == book

def test_renew_missing_loan(client):
    book = add_book(client)
    member = add_member(client)

    result = client.put("/loans/999/renew")

    # A nonexistent loan cannot be renewed.
    assert result.status_code == 404
    assert result.get_json() == {"error": "Loan not found"}

    # The failed renewal should not change existing records.
    assert client.get("/loans").get_json() == []
    assert client.get(f"/books/{book['id']}").get_json() == book
    assert client.get(f"/members/{member['id']}").get_json() == member

def test_checkout_registered_member_preserves_records(client):
    book = add_book(client, copies=2)
    member = add_member(client)

    result = client.post("/loans", json={
        "book_id": book["id"],
        "member_id": member["id"]
    })

    assert result.status_code == 201
    loan = result.get_json()

    # Confirm that the loan belongs to the registered member.
    assert loan["member_id"] == member["id"]
    assert loan["book_id"] == book["id"]

    # The loan should be saved.
    assert client.get("/loans").get_json() == [loan]

    # Only one available copy should be deducted.
    saved_book = client.get(f"/books/{book['id']}")
    assert saved_book.status_code == 200
    assert saved_book.get_json()["available_copies"] == 1

    # Checkout must not modify the member's information.
    saved_member = client.get(f"/members/{member['id']}")
    assert saved_member.get_json() == member














