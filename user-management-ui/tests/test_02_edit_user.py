from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def test_edit_username(driver):
    driver.get("http://localhost:5173/")

    driver.find_element(By.NAME, "username").send_keys("Shanky")
    driver.find_element(By.NAME, "password").send_keys("12345678")
    driver.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))

    # Click Edit button
    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Edit']"))
    )
    driver.execute_script("arguments[0].click();", edit_button)

    # Optional small wait for React render
    time.sleep(5)

    input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='New Username']"))
    )
    input_box.clear()
    time.sleep(5)
    input_box.send_keys("NewShanky")

    time.sleep(5)

    update_button = driver.find_element(By.XPATH, "//button[text()='Update']")
    update_button.click()

    time.sleep(2)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "//td[contains(text(), 'NewShanky')]"), "NewShanky")
    )