from uuid import uuid4

from playwright.sync_api import Page, expect


BASE_URL = "http://" + "127.0.0.1:5000"


def test_add_member_through_browser(page: Page):
    name = "Playwright Test Member"
    email = f"member-{uuid4().hex}@example.com"

    page.goto(f"{BASE_URL}/ui/members")
    page.get_by_label("Name", exact=True).fill(name)
    page.get_by_label("Email", exact=True).fill(email)
    page.get_by_role("button", name="Add Member", exact=True).click()

    email_cell = page.get_by_role("cell", name=email, exact=True)
    member_row = page.get_by_role("row").filter(has=email_cell)
    name_cell = member_row.get_by_role("cell", name=name, exact=True)
    expect(email_cell).to_be_visible()
    expect(name_cell).to_be_visible()


def test_checkout_nonexistent_book_creates_no_loan(page: Page):
    email = f"checkout-{uuid4().hex}@example.com"

    page.goto(f"{BASE_URL}/ui/members")
    page.get_by_label("Name", exact=True).fill("Playwright Checkout Member")
    page.get_by_label("Email", exact=True).fill(email)
    page.get_by_role("button", name="Add Member", exact=True).click()

    email_cell = page.get_by_role("cell", name=email, exact=True)
    member_row = page.get_by_role("row").filter(has=email_cell)
    expect(member_row).to_be_visible()
    member_id = member_row.get_by_role("cell").first.inner_text().strip()

    page.goto(f"{BASE_URL}/ui/loans")
    loan_rows = page.get_by_role("row").filter(has=page.get_by_role("cell"))
    original_count = loan_rows.count()

    page.get_by_label("Book ID", exact=True).fill("-1")
    page.get_by_label("Member ID", exact=True).fill(member_id)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.get_by_role("button", name="Check Out", exact=True).click()

    expect(page.get_by_role("heading", name="Loans", exact=True)).to_be_visible()
    expect(loan_rows).to_have_count(original_count)
