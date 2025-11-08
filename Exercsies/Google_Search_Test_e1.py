from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome driver properly
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Step 1: Navigate to Google
    driver.get("https://www.duckduckgo.com")
    driver.maximize_window()

    # Step 2: Accept cookies or consent (if present)
    try:
        consent_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button//*[contains(text(),'Accept') or contains(text(),'Agree')]/.."))
        )
        consent_btn.click()
    except Exception:
        pass  # no popup, continue

    # Step 3: Find search box and enter search term
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("Selenium WebDriver")
    search_box.send_keys(Keys.RETURN)

    # Step 4: Wait until results appear
    WebDriverWait(driver, 10).until(
        EC.title_contains("Selenium WebDriver")
    )

    # Step 5: Verify result title
    assert "Selenium WebDriver" in driver.title
    print("✅ Test Passed! Title contains 'Selenium WebDriver'")

except AssertionError:
    print("❌ Test Failed! Title mismatch:", driver.title)

except Exception as e:
    print("⚠️ Error during test:", e)

finally:
    driver.quit()
    print("Browser closed.")
