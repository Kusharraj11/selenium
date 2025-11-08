# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

@pytest.fixture(scope="function")
def driver(tmp_path):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")   # comment/uncomment as needed
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)  # increased implicit wait
    # attach a place to save debug artifacts
    driver._debug_dir = os.path.join(str(tmp_path), "debug")
    os.makedirs(driver._debug_dir, exist_ok=True)
    yield driver
    driver.quit()
