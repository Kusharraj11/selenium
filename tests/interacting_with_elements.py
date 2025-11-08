# interacting_with_elements.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Initialize browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Step 2: Open practice website
driver.get("https://rahulshettyacademy.com/AutomationPractice/")
print("Opened:", driver.title)
time.sleep(2)

# ---------- TEXT BOX ---------- #
# Locate input box and type text
input_box = driver.find_element(By.ID, "name")
input_box.send_keys("SoochiTara")
print("Typed name ✅")
time.sleep(1)

# Get and print placeholder text
print("Placeholder text:", input_box.get_attribute("placeholder"))

# Clear the input field
input_box.clear()
print("Cleared input box ✅")
time.sleep(1)

# ---------- RADIO BUTTON ---------- #
# Select radio button option2
radio_btn = driver.find_element(By.XPATH, "//input[@value='radio2']")
radio_btn.click()
print("Clicked Radio Button 2 ✅")
time.sleep(1)

# ---------- CHECKBOX ---------- #
# Click checkbox Option 1
checkbox = driver.find_element(By.ID, "checkBoxOption1")
checkbox.click()
print("Checked Checkbox 1 ✅")
time.sleep(1)

# Uncheck if selected
if checkbox.is_selected():
    checkbox.click()
    print("Unchecked Checkbox 1 ✅")
time.sleep(1)

# ---------- DROPDOWN ---------- #
# Locate dropdown by ID and select by visible text
dropdown = Select(driver.find_element(By.ID, "dropdown-class-example"))
dropdown.select_by_visible_text("Option2")
print("Selected Dropdown Option2 ✅")
time.sleep(1)

# ---------- ALERT ---------- #
# Type a name and click "Alert"
alert_input = driver.find_element(By.ID, "name")
alert_input.send_keys("SoochiTara Alert Test")
driver.find_element(By.ID, "alertbtn").click()
time.sleep(1)

# Switch to alert and accept
alert = driver.switch_to.alert
print("Alert says:", alert.text)
alert.accept()
print("Accepted alert ✅")
time.sleep(1)

# ---------- GET TEXT FROM ELEMENT ---------- #
heading_text = driver.find_element(By.TAG_NAME, "h1").text
print("Page Heading:", heading_text)

# ---------- SUBMIT FORM (if available) ---------- #
# Example: reusing input to submit
input_box = driver.find_element(By.ID, "name")
input_box.send_keys("Submit test")
input_box.submit()  # works if form is present
print("Submitted input field ✅")

# ---------- END ---------- #
time.sleep(2)
driver.quit()
print("Browser closed. Test finished successfully ✅")
