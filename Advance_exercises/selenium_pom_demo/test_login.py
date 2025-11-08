from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from login_page import LoginPage
import time

# --------------------------
# SETUP
# --------------------------
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://the-internet.herokuapp.com/login")
    driver.maximize_window()
    time.sleep(1)

    # --------------------------
    # TEST: Valid login
    # --------------------------
    login_page = LoginPage(driver)
    login_page.login("tomsmith", "SuperSecretPassword!")
    time.sleep(1)

    # Verify successful login by checking URL or heading
    assert "Secure Area" in driver.title or "Secure Area" in driver.page_source
    print("✅ Login test passed!")

    # --------------------------
    # TEST: Invalid login
    # --------------------------
    driver.get("https://the-internet.herokuapp.com/login")
    login_page.login("invalid_user", "invalid_pass")
    time.sleep(1)
    error_message = login_page.get_error_message()
    print("Error message displayed:", error_message)
    assert "Your username is invalid!" in error_message
    print("✅ Invalid login test passed!")

finally:
    driver.quit()
