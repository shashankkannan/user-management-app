from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_delete_user(driver):
    driver.get("http://localhost:5173/")

    # Login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("NewShanky")
    driver.find_element(By.NAME, "password").send_keys("12345678")
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait until dashboard or users table loads (adjust selector accordingly)
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

    # Click Delete button (assumes logged in user can delete their own account)
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Delete']"))
    )
    delete_button.click()

    # Wait for redirect to login page

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Assert login page is shown by checking URL or unique login element
    assert 'Login' in driver.page_source or driver.current_url.endswith("/")