
from uuid import uuid4

from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:5000"


def test_add_book_through_browser(page: Page):
    # Generate a unique title to avoid conflicts with existing records.
    title = f"Playwright Test Book {uuid4().hex[:8]}"

    # Open the book management page.
    page.goto(f"{BASE_URL}/ui/books")

    # Complete the book creation form.
    page.locator('input[name="title"]').fill(title)
    page.locator('input[name="author"]').fill("Test Author")
    page.locator('input[name="isbn"]').fill("9780132350884")
    page.locator('input[name="total_copies"]').fill("3")

    # Submit the form using the specific Add Book button.
    page.get_by_role("button", name="Add Book", exact=True).click()

    # Verify the new book appears with the correct information.
    book_row = page.locator("table tr").filter(has_text=title)

    expect(book_row).to_have_count(1)
    expect(book_row.locator("td").nth(1)).to_have_text(title)
    expect(book_row.locator("td").nth(2)).to_have_text("Test Author")
    expect(book_row.locator("td").nth(4)).to_have_text("3")
    expect(book_row.locator("td").nth(5)).to_have_text("3")

    expect(page).to_have_url(f"{BASE_URL}/ui/books")


def test_delete_single_copy_book(page: Page):
    # Create a single-copy book to test the deletion boundary.
    title = f"Delete Test Book {uuid4().hex[:8]}"

    page.goto(f"{BASE_URL}/ui/books")

    # Create the book as preparation for the deletion workflow.
    page.locator('input[name="title"]').fill(title)
    page.locator('input[name="author"]').fill("Test Author")
    page.locator('input[name="isbn"]').fill("9780132350884")
    page.locator('input[name="total_copies"]').fill("1")

    page.get_by_role("button", name="Add Book", exact=True).click()

    # Find the newly created book and verify its copy counts.
    book_row = page.locator("table tr").filter(has_text=title)

    expect(book_row).to_have_count(1)
    expect(book_row.locator("td").nth(4)).to_have_text("1")
    expect(book_row.locator("td").nth(5)).to_have_text("1")

    # Delete this specific book through the browser.
    book_row.get_by_role("button", name="Delete", exact=True).click()

    # Verify the deleted record is no longer displayed.
    expect(page.locator("table tr").filter(has_text=title)).to_have_count(0)

    # Confirm the user is returned to the Books page.
    expect(page).to_have_url(f"{BASE_URL}/ui/books")
