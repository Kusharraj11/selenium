# waits_demo.py
"""
Waits demo for Selenium (Python).
Copy-paste into VS Code and run:
    python waits_demo.py
Make sure your virtualenv is active and selenium + webdriver-manager are installed.
"""

import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# -------------------------
# Configuration / Defaults
# -------------------------
DEFAULT_IMPLICIT_WAIT = 5    # seconds (if you use implicit waits at all)
DEFAULT_EXPLICIT_TIMEOUT = 15
DEBUG_DIR = os.path.join(os.getcwd(), "debug_waits")
os.makedirs(DEBUG_DIR, exist_ok=True)


def save_debug(driver, name="debug"):
    """Save screenshot and page source for debugging."""
    ts = time.strftime("%Y%m%d-%H%M%S")
    png = os.path.join(DEBUG_DIR, f"{name}-{ts}.png")
    html = os.path.join(DEBUG_DIR, f"{name}-{ts}.html")
    try:
        driver.save_screenshot(png)
        with open(html, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"[debug saved] {png}")
        print(f"[debug saved] {html}")
    except Exception as e:
        print("Failed to save debug:", e)


def init_driver(implicit_wait=None, headless=False):
    """Initialize Chrome driver with optional implicit wait."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    if implicit_wait is not None:
        driver.implicitly_wait(implicit_wait)
        print(f"[init] implicit wait set to {implicit_wait}s")
    return driver


# -------------------------
# DEMO: implicit wait
# -------------------------
def demo_implicit_wait():
    """
    Implicit wait example: driver implicitly waits up to X seconds when locating elements.
    Not recommended as sole strategy for dynamic content.
    """
    print("\n--- demo_implicit_wait ---")
    driver = init_driver(implicit_wait=DEFAULT_IMPLICIT_WAIT)
    try:
        driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        print("Page opened:", driver.title)
        # Suppose element appears after X seconds; implicit wait will retry find_element
        try:
            el = driver.find_element(By.ID, "name")  # quick present element
            print("Found element by ID (implicit):", el.tag_name)
        except Exception as e:
            print("Implicit find failed:", e)
    finally:
        driver.quit()


# -------------------------
# DEMO: explicit wait (recommended)
# -------------------------
def demo_explicit_waits():
    """
    Explicit waits demonstrate common conditions using WebDriverWait + expected_conditions.
    More reliable and recommended for dynamic pages.
    """
    print("\n--- demo_explicit_waits ---")
    driver = init_driver(implicit_wait=0)  # set implicit to 0 when using explicit waits (recommended)
    wait = WebDriverWait(driver, DEFAULT_EXPLICIT_TIMEOUT)

    try:
        driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        # 1) Wait for presence (in DOM) of input[name='name']
        el = wait.until(EC.presence_of_element_located((By.ID, "name")))
        print("presence_of_element_located: found", el.get_attribute("id"))

        # 2) Wait for visibility (visible and height/width > 0)
        visible_el = wait.until(EC.visibility_of_element_located((By.ID, "name")))
        print("visibility_of_element_located: visible ->", visible_el.tag_name)

        # 3) Wait for element to be clickable
        # Example: the button that shows/hides might become clickable later
        clickable_el = wait.until(EC.element_to_be_clickable((By.ID, "alertbtn")))
        print("element_to_be_clickable: OK ->", clickable_el.get_attribute("id"))

        # 4) Wait for text to be present in element after clicking (simulate dynamic text change)
        # We'll trigger an alert which shows a JS alert (can't directly wait text change on alert).
        # Instead we will click a button and then wait for page title to remain or other condition as an example.
        driver.find_element(By.ID, "alertbtn").click()
        # Switch to alert and accept
        alert = wait.until(EC.alert_is_present())
        print("Alert text:", alert.text)
        alert.accept()
        print("Alert accepted via explicit wait.")

        # 5) Wait for invisibility or staleness (useful when waiting for overlays to disappear)
        # For demo: click 'Hide' and wait till element is not visible
        driver.find_element(By.ID, "displayed-text").is_displayed()  # may be present
        driver.find_element(By.ID, "hide-textbox").click()
        wait.until(EC.invisibility_of_element_located((By.ID, "displayed-text")))
        print("invisibility_of_element_located: input hidden")

    except Exception as e:
        print("Exception during explicit waits demo:", e)
        traceback.print_exc()
        save_debug(driver, "explicit_waits_failure")
        raise
    finally:
        driver.quit()


# -------------------------
# DEMO: fluent wait (custom poll frequency)
# -------------------------
def demo_fluent_wait():
    """
    Fluent-style wait using WebDriverWait with a custom poll_frequency.
    WebDriverWait already supports poll_frequency; this is the 'fluent' style.
    """
    print("\n--- demo_fluent_wait ---")
    driver = init_driver(implicit_wait=0)
    # poll every 0.5s, timeout 20s
    wait = WebDriverWait(driver, 20, poll_frequency=0.5, ignored_exceptions=[Exception])

    try:
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")
        print("Page opened:", driver.title)
        # Click the start button which begins a dynamic load
        driver.find_element(By.CSS_SELECTOR, "#start button").click()
        # Wait until the loading finishes and the element with id 'finish' is visible
        finish = wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        print("Fluent wait: found text ->", finish.text)
    except Exception as e:
        print("Exception in fluent wait demo:", e)
        traceback.print_exc()
        save_debug(driver, "fluent_waits_failure")
        raise
    finally:
        driver.quit()


# -------------------------
# DEMO: custom ExpectedCondition
# -------------------------
class element_has_non_empty_text:
    """
    Example of creating a custom ExpectedCondition that checks for non-empty text inside element.
    WebDriverWait will call this until it returns a truthy value or times out.
    Usage: WebDriverWait(driver, timeout).until(element_has_non_empty_text((By.ID, 'msg')))
    """

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            el = driver.find_element(*self.locator)
            text = el.text.strip()
            if text:
                return el
            return False
        except Exception:
            return False


def demo_custom_expected_condition():
    print("\n--- demo_custom_expected_condition ---")
    driver = init_driver(implicit_wait=0)
    wait = WebDriverWait(driver, 20, poll_frequency=0.5)
    try:
        driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
        driver.find_element(By.CSS_SELECTOR, "#start button").click()
        # Wait until #finish has non-empty text
        el = wait.until(element_has_non_empty_text((By.ID, "finish")))
        print("Custom condition: text is ->", el.text)
    except Exception as e:
        print("Custom condition failed:", e)
        save_debug(driver, "custom_condition_failure")
        raise
    finally:
        driver.quit()


# -------------------------
# RUN DEMOS
# -------------------------
if __name__ == "__main__":
    # Run in sequence — each demo creates and destroys its own driver.
    # You can comment out ones you don't want to run.
    demo_implicit_wait()
    demo_explicit_waits()
    demo_fluent_wait()
    demo_custom_expected_condition()
    print("\nAll demos complete. Check debug directory if any failures:", DEBUG_DIR)
