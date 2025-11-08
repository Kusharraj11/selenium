# keyboard_no_input_fix.py
"""
Robust helper to diagnose & fix send_keys() 'no input' problems.
Saves debug artifacts to debug/ if it fails.
Run: python keyboard_no_input_fix.py
"""

import os, time, traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

DEBUG_DIR = os.path.join(os.getcwd(), "debug")
os.makedirs(DEBUG_DIR, exist_ok=True)

def save_debug(driver, name="debug"):
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
        print("Failed to save debug artifacts:", e)

def try_send_keys_standard(el, text):
    try:
        el.clear()
    except Exception:
        pass
    el.send_keys(text)

def try_send_keys_with_click(el, text):
    el.click()
    time.sleep(0.2)
    el.send_keys(text)

def try_actionchains(el, text, driver):
    actions = ActionChains(driver)
    actions.move_to_element(el).click().send_keys(text).perform()

def try_js_set_value(el, text, driver):
    script = "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));"
    driver.execute_script(script, el, text)

def find_input_and_send(driver, locator, text):
    wait = WebDriverWait(driver, 8)
    # Try presence and visibility
    el = wait.until(EC.presence_of_element_located(locator))
    # If inside iframe, frame_to_be_available_and_switch_to_it will help, but can't know until we find element.
    # We'll return the located element (might be stale if switching required).
    return el

def switch_to_iframe_if_needed(driver):
    # Try to detect iframe that contains the #target input by searching in each iframe
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    if not frames:
        return False
    for i, f in enumerate(frames):
        try:
            driver.switch_to.frame(f)
            # quick check: is our input present?
            if driver.find_elements(By.ID, "target"):
                print(f"Found input inside iframe index {i} — switched into it.")
                return True
            driver.switch_to.default_content()
        except Exception:
            driver.switch_to.default_content()
    return False

def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # avoid headless while debugging
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        driver.get("https://the-internet.herokuapp.com/key_presses")
        print("Opened:", driver.title)
        wait = WebDriverWait(driver, 8)

        locator = (By.ID, "target")
        # First try: visible & clickable
        try:
            input_box = wait.until(EC.element_to_be_clickable(locator))
            print("Input found & clickable ✅")
        except Exception:
            # Maybe inside iframe — try switching
            print("Input not clickable / not found directly. Checking if inside iframe...")
            switched = switch_to_iframe_if_needed(driver)
            if switched:
                # after switching, try again to find clickable element
                input_box = wait.until(EC.element_to_be_clickable(locator))
            else:
                # fallback: try presence
                input_box = wait.until(EC.presence_of_element_located(locator))
            print("Located input after iframe check.")

        # Try #1: standard send_keys after clear()
        try:
            print("Attempt 1: standard send_keys()")
            try_send_keys_standard(input_box, "Hello1")
            time.sleep(0.5)
            current = input_box.get_attribute("value") or input_box.text
            print("Value after attempt 1:", repr(current))
            if "Hello1" in (current or ""):
                print("Success on attempt 1 ✅")
                return
        except Exception as e:
            print("Attempt1 exception:", e)

        # Try #2: click then send_keys
        try:
            print("Attempt 2: click() then send_keys()")
            try_send_keys_with_click(input_box, "Hello2")
            time.sleep(0.5)
            current = input_box.get_attribute("value") or input_box.text
            print("Value after attempt 2:", repr(current))
            if "Hello2" in (current or ""):
                print("Success on attempt 2 ✅")
                return
        except Exception as e:
            print("Attempt2 exception:", e)

        # Try #3: ActionChains
        try:
            print("Attempt 3: ActionChains move/click/send_keys")
            try_actionchains(input_box, "Hello3", driver)
            time.sleep(0.5)
            current = input_box.get_attribute("value") or input_box.text
            print("Value after attempt 3:", repr(current))
            if "Hello3" in (current or ""):
                print("Success on attempt 3 ✅")
                return
        except Exception as e:
            print("Attempt3 exception:", e)

        # Try #4: JS set value (last resort)
        try:
            print("Attempt 4: Setting value via JavaScript")
            try_js_set_value(input_box, "Hello4", driver)
            time.sleep(0.5)
            current = input_box.get_attribute("value") or input_box.text
            print("Value after attempt 4:", repr(current))
            if "Hello4" in (current or ""):
                print("Success on attempt 4 ✅")
                return
        except Exception as e:
            print("Attempt4 exception:", e)

        # If none worked, save debug artifacts
        print("All attempts failed — saving debug artifacts.")
        save_debug(driver, "no_input_failure")
        raise RuntimeError("send_keys did not input any text after multiple attempts.")

    except Exception as e:
        print("Error during demo:", e)
        traceback.print_exc()
        try:
            save_debug(driver, "exception")
        except Exception:
            pass
    finally:
        time.sleep(2)
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
