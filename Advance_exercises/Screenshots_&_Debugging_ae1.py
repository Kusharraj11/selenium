# screenshots_debugging.py
"""
Screenshots & Debugging demo for Selenium (VS Code copy-paste).
Demonstrates:
 - full page screenshot
 - element screenshot
 - save page source to file
 - execute JavaScript (scroll, read innerHTML)
 - save debug artifacts into debug/ with timestamps
"""

import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

DEBUG_DIR = os.path.join(os.getcwd(), "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

def ts():
    return time.strftime("%Y%m%d-%H%M%S")

def save_page_source(driver, prefix="page"):
    filename = os.path.join(DEBUG_DIR, f"{prefix}-{ts()}.html")
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"[saved] page source -> {filename}")
    except Exception as e:
        print("Failed to save page source:", e)

def save_screenshot(driver, prefix="screenshot"):
    filename = os.path.join(DEBUG_DIR, f"{prefix}-{ts()}.png")
    try:
        driver.save_screenshot(filename)
        print(f"[saved] full page screenshot -> {filename}")
    except Exception as e:
        print("Failed to save screenshot:", e)

def save_element_screenshot(element, prefix="element"):
    filename = os.path.join(DEBUG_DIR, f"{prefix}-{ts()}.png")
    try:
        element.screenshot(filename)
        print(f"[saved] element screenshot -> {filename}")
    except Exception as e:
        print("Failed to save element screenshot:", e)

def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # optionally run headless
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    wait = WebDriverWait(driver, 12)

    try:
        driver.get("https://the-internet.herokuapp.com/large")
        print("Opened page:", driver.title)

        # 1) Full page screenshot
        time.sleep(1)  # short pause to ensure rendering
        save_screenshot(driver, prefix="page_full")

        # 2) Scroll down using JS, then take another screenshot
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.8)
        save_screenshot(driver, prefix="page_scrolled")

        # 3) Find an element and take an element-level screenshot
        # Use a stable locator; fallback if not present
        try:
            # example element on page: header
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.example h3")))
            print("Found element for screenshot:", element.text)
            save_element_screenshot(element, prefix="header")
        except Exception:
            print("Could not locate the element for element screenshot.")

        # 4) Save page source to a file
        save_page_source(driver, prefix="page_source")

        # 5) Execute JS to get innerHTML of an element
        try:
            el_for_js = driver.find_element(By.CSS_SELECTOR, "div.example")
            inner_html = driver.execute_script("return arguments[0].innerHTML;", el_for_js)
            # Save innerHTML to a file
            html_file = os.path.join(DEBUG_DIR, f"innerHTML-{ts()}.html")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(inner_html)
            print(f"[saved] innerHTML -> {html_file}")
        except Exception as e:
            print("JS innerHTML extraction failed:", e)

        # 6) Example: get element properties via JS (bounding rect)
        try:
            rect = driver.execute_script(
                "const r = arguments[0].getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height};",
                el_for_js
            )
            print("Element bounding rect (via JS):", rect)
        except Exception:
            print("Failed to get bounding rect via JS.")

        # 7) Additional: take screenshot of an input after typing (if any input on page)
        # (demonstrates taking screenshot after interaction)
        try:
            # goto a page with input
            driver.get("https://the-internet.herokuapp.com/login")
            usr = wait.until(EC.presence_of_element_located((By.ID, "username")))
            usr.send_keys("tomsmith")
            save_element_screenshot(usr, prefix="username_input")
        except Exception as e:
            print("Input interaction screenshot failed:", e)

        print("\nAll debug artifacts saved in:", DEBUG_DIR)

    except Exception as e:
        print("Exception during debug run:", e)
        traceback.print_exc()
        # try to save debug artifacts on failure
        try:
            save_screenshot(driver, prefix="failure")
            save_page_source(driver, prefix="failure")
        except Exception:
            pass
    finally:
        time.sleep(1)
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
