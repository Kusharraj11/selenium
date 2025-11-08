# tests/test_google_search.py
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _try_click_any(driver, wait, xpaths):
    """Try several xpaths; return True if clicked one, else False."""
    for xp in xpaths:
        try:
            el = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            el.click()
            return True
        except Exception:
            # skip and try next
            continue
    return False

def _save_debug(driver, name_prefix="failure"):
    """Save screenshot and page source to driver's debug folder (from conftest tmp_path)."""
    try:
        ts = time.strftime("%Y%m%d-%H%M%S")
        folder = getattr(driver, "_debug_dir", None) or "."
        png = f"{folder}/{name_prefix}-{ts}.png"
        html = f"{folder}/{name_prefix}-{ts}.html"
        driver.save_screenshot(png)
        with open(html, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"[debug saved] screenshot: {png}")
        print(f"[debug saved] page source: {html}")
    except Exception as e:
        print("Failed to save debug info:", e)

def test_google_search(driver):
    wait = WebDriverWait(driver, 15)  # explicit wait for key elements
    try:
        driver.get("https://www.google.com")

        # Try to accept cookie/consent/popups — common variants:
        consent_xpaths = [
            "//button[.//div[contains(text(),'I agree') or contains(text(),'I Agree')]]",
            "//button//*[contains(text(),'Agree')]/..",
            "//button[contains(text(),'Accept')]",
            "//div[contains(text(),'I agree')]/ancestor::button",
            "//button[@id='L2AGLb' or @id='introAgreeButton']",
            "//button[contains(@aria-label,'Accept all')]",
            "//form//button[contains(., 'Accept all')]",
            # fallback: a generic button with Accept or Agree text
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
        ]
        clicked = _try_click_any(driver, wait, consent_xpaths)
        if clicked:
            # short pause to let overlay disappear
            time.sleep(0.5)

        # Wait for the search input. Using CSS selector is more stable here.
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))
        search_box.clear()
        search_box.send_keys("Selenium WebDriver")
        search_box.send_keys(Keys.RETURN)

        # Wait for title to contain the search term
        wait.until(EC.title_contains("Selenium WebDriver"))
        assert "Selenium WebDriver" in driver.title

    except Exception as e:
        # Save screenshot + page source to help debug
        print("TEST EXCEPTION:", e)
        traceback.print_exc()
        _save_debug(driver, name_prefix="test_google_search_failure")
        raise
