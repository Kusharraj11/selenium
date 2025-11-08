# multiple_windows_test.py
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
    driver.get("https://the-internet.herokuapp.com/windows")
    print("Opened:", driver.title)

    wait = WebDriverWait(driver, 10)

    # Step 3: Store the original window handle
    original_window = driver.current_window_handle
    print("Original window handle stored ✅")

    # Step 4: Click link to open a new window/tab
    driver.find_element(By.LINK_TEXT, "Click Here").click()
    print("Clicked 'Click Here' link ✅")

    # Step 5: Wait for new window to open (total windows = 2)
    wait.until(EC.number_of_windows_to_be(2))
    print("New window detected ✅")

    # Step 6: Switch to the new window
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    print("Switched to new window ✅")

    # Step 7: Verify new window content
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
    assert "New Window" in driver.page_source
    print("Verified new window text: 'New Window' ✅")

    # Step 8: Close new window
    driver.close()
    print("Closed new window ✅")

    # Step 9: Switch back to original window
    driver.switch_to.window(original_window)
    print("Switched back to original window ✅")

    # Step 10: Verify original page title
    assert "The Internet" in driver.title
    print("✅ Test Passed — Original window verified successfully!")

except AssertionError:
    print("❌ Test Failed — Text or title verification failed.")
except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")
