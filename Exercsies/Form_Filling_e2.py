# form_filling_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Initialize Chrome browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    # Step 2: Open the test website
    driver.get("https://www.selenium.dev/selenium/web/web-form.html")
    print("Opened:", driver.title)

    wait = WebDriverWait(driver, 10)

    # Step 3: Fill in the text input field
    text_input = wait.until(EC.presence_of_element_located((By.NAME, "my-text")))
    text_input.send_keys("SoochiTara")
    print("Entered text ✅")

    # Step 4: Enter password in password field
    password_field = driver.find_element(By.NAME, "my-password")
    password_field.send_keys("secret123")
    print("Entered password ✅")

    # Step 5: Enter text in textarea
    textarea = driver.find_element(By.NAME, "my-textarea")
    textarea.send_keys("This is a Selenium form-filling test.")
    print("Entered textarea text ✅")

    # Step 6: Select an option from dropdown
    dropdown = Select(driver.find_element(By.NAME, "my-select"))
    dropdown.select_by_visible_text("Option 2")
    print("Selected dropdown option ✅")

    # Step 7: Click checkbox
    checkbox = driver.find_element(By.ID, "my-check-1")
    checkbox.click()
    print("Clicked checkbox ✅")

    # Step 8: Click submit button
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()
    print("Clicked submit ✅")

    # Step 9: Verify success message
    success_msg = wait.until(EC.visibility_of_element_located((By.ID, "message")))
    msg_text = success_msg.text
    print("Success message:", msg_text)

    assert "received" in msg_text.lower()
    print("✅ Test Passed — form submitted successfully!")

except AssertionError:
    print("❌ Test Failed — success message not found.")
except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")
