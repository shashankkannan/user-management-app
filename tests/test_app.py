from playwright.sync_api import sync_playwright
import pytest

BASE_URL = "http://localhost:5173"

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # set headless=True for CI
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

def test_login_edit_delete_flow(page):
 
    page.goto(f"{BASE_URL}/")
    page.fill('input[name="username"]', "Shanky")
    page.fill('input[name="password"]', "12345678")
    page.click('button:has-text("Login")')

    page.wait_for_url(f"{BASE_URL}/dashboard")
    page.wait_for_selector("h2:has-text('All Users')")
    user_id = page.evaluate("() => localStorage.getItem('user_id')")

    assert user_id is not None

    
    edit_btn_selector = f'tr:has(td:text("{user_id}")) button:has-text("Edit")'
    page.click(edit_btn_selector)
    page.fill('form input[placeholder="New Username"]', "NewShanky")
    page.click('form button:has-text("Update")')
    page.wait_for_timeout(1000)  # wait for update or better wait for network

    assert page.locator(f'td:text("NewShanky")').count() > 0

    
    page.click('button:has-text("Logout")')
    page.wait_for_timeout(1000)

    page.fill('input[name="username"]', "NewShanky")
    page.fill('input[name="password"]', "12345678")
    page.click('button:has-text("Login")')
    page.wait_for_timeout(2000)

    page.wait_for_url(f"{BASE_URL}/dashboard")

    delete_btn_selector = f'tr:has(td:text("{user_id}")) button:has-text("Delete")'
    page.click(delete_btn_selector)

    page.wait_for_url(f"{BASE_URL}/")

    token = page.evaluate("() => localStorage.getItem('token')")

    assert token is None