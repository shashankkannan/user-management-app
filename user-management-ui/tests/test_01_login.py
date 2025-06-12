from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_login_success(driver):
    driver.get("http://localhost:5173/")

    driver.find_element("name", "username").send_keys("Shanky")
    driver.find_element("name", "password").send_keys("12345678")
    driver.find_element("tag name", "button").click()

  
    WebDriverWait(driver, 5).until(
        lambda d: "/dashboard" in d.current_url or "Login failed" in d.page_source
    )

    print("Current URL:", driver.current_url)
    print("Page Output:\n", driver.page_source[:1000])  # Limit output

    assert "/dashboard" in driver.current_url
