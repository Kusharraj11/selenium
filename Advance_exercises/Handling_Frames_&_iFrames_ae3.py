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
    driver.get("https://the-internet.herokuapp.com/iframe")
    print("Opened:", driver.title)

    wait = WebDriverWait(driver, 10)

    # Step 3: Wait for iframe to load
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "mce_0_ifr")))
    print("Switched into iframe ✅")

    # Step 4: Wait for the editor body to become clickable/editable
    editor_body = wait.until(EC.element_to_be_clickable((By.ID, "tinymce")))

    # Clear old text safely using JavaScript (avoids invalid element state)
    driver.execute_script("arguments[0].innerHTML = '';", editor_body)
    editor_body.send_keys("Hello SoochiTara — text entered safely into TinyMCE iframe!")
    print("Typed text inside iframe ✅")

    # Step 5: Switch back to main content
    driver.switch_to.default_content()
    print("Switched back to main page ✅")

    # Step 6: Verify header outside the iframe
    header = driver.find_element(By.TAG_NAME, "h3").text
    assert "Editor" in header
    print("Verified header:", header)

    print("\n✅ Test Passed — iFrame handled successfully!")

except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")
