# mouse_actions_test.py
"""
Exercise 9 : Mouse Actions – Using ActionChains
Website used (for hover demo): https://the-internet.herokuapp.com/hovers
Also demonstrates:
  - Hover over elements
  - Double click
  - Right click
  - Drag and drop
  - Chaining multiple actions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Initialize browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
actions = ActionChains(driver)
wait = WebDriverWait(driver, 10)

try:
    # ---------- HOVER ACTION ----------
    driver.get("https://the-internet.herokuapp.com/hovers")
    print("Opened:", driver.title)

    # Hover over the first image card
    figure = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.figure")))
    actions.move_to_element(figure).perform()
    print("Hovered over element ✅")
    time.sleep(1)

    # ---------- DOUBLE CLICK & RIGHT CLICK (using JS demo site) ----------
    driver.get("https://testautomationpractice.blogspot.com/")
    print("Opened Double/Right Click Demo")

    # Double click example – button with ID "field2"
    field1 = wait.until(EC.presence_of_element_located((By.ID, "field1")))
    field1.clear()
    field1.send_keys("SoochiTara")
    copy_button = driver.find_element(By.XPATH, "//button[text()='Copy Text']")
    actions.double_click(copy_button).perform()
    print("Performed double click ✅")
    time.sleep(1)

    # Right click on "Copy Text" button
    actions.context_click(copy_button).perform()
    print("Performed right click ✅")
    time.sleep(1)

    # ---------- DRAG AND DROP ----------
    driver.get("https://the-internet.herokuapp.com/drag_and_drop")
    print("Opened Drag and Drop Demo")

    source = wait.until(EC.presence_of_element_located((By.ID, "column-a")))
    target = driver.find_element(By.ID, "column-b")
    actions.drag_and_drop(source, target).perform()
    print("Drag and drop performed ✅")
    time.sleep(1)

    # ---------- CHAIN MULTIPLE ACTIONS ----------
    driver.get("https://the-internet.herokuapp.com/login")
    print("Opened Login Page for chained actions demo")

    username = wait.until(EC.presence_of_element_located((By.ID, "username")))
    actions.move_to_element(username).click().send_keys("tomsmith").perform()
    print("Chained actions executed ✅")

    print("\n✅ Test Passed — All mouse actions performed successfully!")

except Exception as e:
    print("⚠️ Error during test:", e)
finally:
    time.sleep(2)
    driver.quit()
    print("Browser closed.")
