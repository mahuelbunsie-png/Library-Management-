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
