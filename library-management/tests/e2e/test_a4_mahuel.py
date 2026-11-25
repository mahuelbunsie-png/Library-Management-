
from uuid import uuid4

from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:5000"


def test_add_book_through_browser(page: Page):
    # Use a unique title so the test is independent of existing books.
    title = f"Playwright Test Book {uuid4().hex[:8]}"

    # Open the library's book management page.
    page.goto(f"{BASE_URL}/ui/books")

    # Fill out the form as a user would.
    page.locator('input[name="title"]').fill(title)
    page.locator('input[name="author"]').fill("Test Author")
    page.locator('input[name="isbn"]').fill("9780132350884")
    page.locator('input[name="total_copies"]').fill("3")

    # Submit the form and verify the book appears.
    page.locator('button[type="submit"]').click()

    expect(page.get_by_text(title)).to_be_visible()



def test_reject_book_with_zero_copies(page: Page):
    title = f"Invalid Book {uuid4().hex[:8]}"

    page.goto(f"{BASE_URL}/ui/books")

    # Record the number of books before attempting submission.
    book_rows = page.locator("table tr")
    original_count = book_rows.count()

    # Complete the form with an invalid copy count.
    page.locator('input[name="title"]').fill(title)
    page.locator('input[name="author"]').fill("Test Author")
    page.locator('input[name="isbn"]').fill("9780132350884")

    copies_input = page.locator('input[name="total_copies"]')
    copies_input.fill("0")

    # Attempt to submit the form through the browser.
    page.get_by_role("button", name="Add Book").click()

    # HTML validation should prevent the form from being submitted.
    assert copies_input.evaluate(
        "(element) => element.validity.rangeUnderflow"
    )

    # The user should remain on the book management page.
    expect(page).to_have_url(f"{BASE_URL}/ui/books")

    # No new book should appear in the table.
    expect(book_rows).to_have_count(original_count)
    expect(
        page.locator("table tr").filter(has_text=title)
    ).to_have_count(0)
