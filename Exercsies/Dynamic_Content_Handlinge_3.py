# dynamic_content_test.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Initialize Chrome browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    # Step 2: Open the test website
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
    print("Opened:", driver.title)

    # Step 3: Click the "Start" button
    start_button = driver.find_element(By.CSS_SELECTOR, "#start button")
    start_button.click()
    print("Clicked Start ✅")

    # Step 4: Wait for loading bar to disappear (invisibility)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.invisibility_of_element_located((By.ID, "loading")))
    print("Loading bar disappeared ✅")

    # Step 5: Wait for the text "Hello World!" to appear
    finish_element = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish"))
    )

    # Step 6: Verify and print the text
    result_text = finish_element.text
    print("Result text found:", result_text)

    assert result_text == "Hello World!"
    print("✅ Test Passed — Text is displayed correctly!")

except AssertionError:
    print("❌ Test Failed — Text did not match.")
except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")
