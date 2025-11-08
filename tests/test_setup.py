# test_setup.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # uncomment to run headless
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get("https://www.google.com")
        print("Page Title:", driver.title)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
