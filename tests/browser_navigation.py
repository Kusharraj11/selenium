# browser_navigation.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Initialize Chrome browser
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment if you don’t want the browser to show
driver = webdriver.Chrome(service=service, options=options)

# Step 2: Maximize window
driver.maximize_window()

# Step 3: Open a website
driver.get("https://www.google.com")
print("Opened site:", driver.title)
time.sleep(2)

# Step 4: Navigate to another site
driver.get("https://www.bing.com")
print("Now at:", driver.title)
time.sleep(2)

# Step 5: Go back to previous page
driver.back()
print("Went back to:", driver.title)
time.sleep(2)

# Step 6: Go forward again
driver.forward()
print("Went forward to:", driver.title)
time.sleep(2)

# Step 7: Refresh the page
driver.refresh()
print("Page refreshed!")
time.sleep(2)

# Step 8: Close the browser window
driver.close()        # closes current tab
driver.quit()         # closes the browser completely

print("Browser closed successfully ✅")
