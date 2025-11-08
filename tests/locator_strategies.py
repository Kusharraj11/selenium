# locator_strategies.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Initialize Chrome browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Step 2: Open test website
driver.get("https://www.saucedemo.com/")
print("Opened:", driver.title)
time.sleep(2)

# ---------- LOCATOR STRATEGIES DEMO ---------- #

# 1️⃣ Locate by ID
username_box = driver.find_element(By.ID, "user-name")
username_box.send_keys("standard_user")
print("Located by ID ✅")

# 2️⃣ Locate by NAME
password_box = driver.find_element(By.NAME, "password")
password_box.send_keys("secret_sauce")
print("Located by NAME ✅")

# 3️⃣ Locate by CLASS NAME
login_btn = driver.find_element(By.CLASS_NAME, "submit-button")
login_btn.click()
print("Located by CLASS NAME ✅")
time.sleep(2)

# 4️⃣ Locate by TAG NAME
# Example: Find all <a> tags (links)
all_links = driver.find_elements(By.TAG_NAME, "a")
print(f"Located by TAG NAME ✅ - Total links found: {len(all_links)}")

# 5️⃣ Locate by LINK TEXT
menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
menu_button.click()
time.sleep(1)
about_link = driver.find_element(By.LINK_TEXT, "About")
print("Located by LINK TEXT ✅ - Found 'About' link")

# 6️⃣ Locate by PARTIAL LINK TEXT
logout_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Logout")
print("Located by PARTIAL LINK TEXT ✅ - Found Logout link")

# 7️⃣ Locate by CSS SELECTOR
# Let's click on the All Items link in the sidebar
all_items_link = driver.find_element(By.CSS_SELECTOR, "a#inventory_sidebar_link")
print("Located by CSS SELECTOR ✅ - Found All Items link")

# 8️⃣ Locate by XPATH
# Example: find the shopping cart link
cart_icon = driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']")
cart_icon.click()
print("Located by XPATH ✅ - Clicked cart icon")

time.sleep(2)

# ---------- END DEMO ---------- #
driver.quit()
print("Test completed successfully ✅")
