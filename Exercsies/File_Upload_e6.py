# file_upload_test.py
"""
Exercise 6: File Upload
Website: https://the-internet.herokuapp.com/upload
Steps:
1. Create a test file
2. Upload it using send_keys()
3. Click upload button
4. Verify success message
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Step 1: Create a temporary test file
file_name = "test_file.txt"
file_path = os.path.abspath(file_name)

with open(file_path, "w") as f:
    f.write("This is a test file uploaded using Selenium WebDriver.\n")
print(f"Created test file: {file_path}")

# Step 2: Initialize Chrome browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

try:
    # Step 3: Open upload test page
    driver.get("https://the-internet.herokuapp.com/upload")
    print("Opened:", driver.title)

    wait = WebDriverWait(driver, 10)

    # Step 4: Locate file input and upload file
    upload_input = wait.until(EC.presence_of_element_located((By.ID, "file-upload")))
    upload_input.send_keys(file_path)
    print("File selected for upload ✅")

    # Step 5: Click upload button
    upload_button = driver.find_element(By.ID, "file-submit")
    upload_button.click()
    print("Clicked upload button ✅")

    # Step 6: Wait for confirmation
    uploaded_text = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h3")))
    result = uploaded_text.text
    print("Upload message:", result)

    # Step 7: Verify upload success
    assert "File Uploaded!" in result
    uploaded_file_name = driver.find_element(By.ID, "uploaded-files").text
    print(f"Uploaded file confirmed: {uploaded_file_name}")
    assert uploaded_file_name == file_name
    print("✅ Test Passed — File uploaded successfully!")

except AssertionError:
    print("❌ Test Failed — File upload verification failed.")
except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")

    # Optional: Clean up test file
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted test file: {file_path}")
