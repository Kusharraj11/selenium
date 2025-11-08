# alerts_popups_test.py
"""
Exercise 7: Handling Alerts & Pop-ups
Website: https://the-internet.herokuapp.com/javascript_alerts
Steps:
 1. Handle a simple alert
 2. Handle a confirmation alert (accept and dismiss)
 3. Handle a prompt alert (send text)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
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
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    print("Opened:", driver.title)

    wait = WebDriverWait(driver, 10)

    # ---------- SIMPLE ALERT ---------- #
    print("\nHandling Simple Alert...")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()

    alert = wait.until(EC.alert_is_present())
    print("Alert text:", alert.text)
    alert.accept()
    print("✅ Simple alert accepted.")

    # ---------- CONFIRM ALERT ---------- #
    print("\nHandling Confirm Alert...")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()

    alert = wait.until(EC.alert_is_present())
    print("Alert text:", alert.text)
    alert.dismiss()  # You can change to alert.accept() to click OK
    print("✅ Confirm alert dismissed.")

    # Verify alert result text on page
    result_text = driver.find_element(By.ID, "result").text
    print("Result message after dismiss:", result_text)

    # ---------- PROMPT ALERT ---------- #
    print("\nHandling Prompt Alert...")
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()

    alert = wait.until(EC.alert_is_present())
    print("Prompt text:", alert.text)
    alert.send_keys("SoochiTara Test Input")
    alert.accept()
    print("✅ Prompt alert accepted with input.")

    # Verify prompt result text
    result_text = driver.find_element(By.ID, "result").text
    print("Result message after prompt:", result_text)

    # Assertion example (optional)
    assert "SoochiTara" in result_text
    print("\n✅ Test Passed — All alerts handled successfully!")

except AssertionError:
    print("❌ Test Failed — Verification text mismatch.")
except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")
