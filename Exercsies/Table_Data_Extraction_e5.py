# table_data_extraction.py
"""
Exercise 5: Table Data Extraction
- Extract all data from Table 1 on https://the-internet.herokuapp.com/tables
- Find the person with the highest due amount
- Print all email addresses
- Count total number of rows
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

def parse_currency_to_float(s: str) -> float:
    """Convert currency string like '$100.00' or '$1,234.56' to float."""
    if s is None:
        return 0.0
    # Remove currency symbols, commas, whitespace, parentheses
    s = s.strip()
    # handle parentheses for negative amounts e.g. ($1,234.56)
    negative = False
    if s.startswith('(') and s.endswith(')'):
        negative = True
        s = s[1:-1]
    # remove anything not digit or dot or minus
    cleaned = re.sub(r'[^0-9.\-]', '', s)
    try:
        val = float(cleaned) if cleaned else 0.0
    except ValueError:
        val = 0.0
    return -val if negative else val

def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    try:
        driver.get("https://the-internet.herokuapp.com/tables")
        wait = WebDriverWait(driver, 10)
        # Wait for table1 to be present
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table1")))

        rows = driver.find_elements(By.CSS_SELECTOR, "#table1 tbody tr")
        total_rows = len(rows)
        print(f"Total rows found in Table 1: {total_rows}")

        people = []
        emails = []

        for i, row in enumerate(rows, start=1):
            cells = row.find_elements(By.TAG_NAME, "td")
            # Defensive checks in case table structure changes
            if len(cells) < 6:
                print(f"Row {i} unexpected cell count ({len(cells)}). Skipping.")
                continue

            last_name = cells[0].text.strip()
            first_name = cells[1].text.strip()
            email = cells[2].text.strip()
            due_raw = cells[3].text.strip()
            website = cells[4].text.strip() if len(cells) > 4 else ""
            action = cells[5].text.strip() if len(cells) > 5 else ""

            due_value = parse_currency_to_float(due_raw)

            people.append({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "due_raw": due_raw,
                "due": due_value,
                "website": website,
                "action": action
            })
            emails.append(email)

            print(f"Row {i}: {first_name} {last_name} | Email: {email} | Due: {due_raw} -> {due_value}")

        if not people:
            print("No people parsed from the table.")
            return

        # Find person with highest due
        highest = max(people, key=lambda p: p["due"])
        print("\nPerson with the highest due:")
        print(f"{highest['first_name']} {highest['last_name']} — Email: {highest['email']} — Due: {highest['due_raw']} ({highest['due']})")

        # Print all email addresses (unique)
        unique_emails = sorted(set(emails))
        print("\nAll email addresses (unique):")
        for e in unique_emails:
            print("-", e)

        print(f"\nTotal rows (counted): {total_rows}")
        print("Done ✅")

    except Exception as e:
        print("Error during extraction:", e)
    finally:
        time.sleep(1)
        driver.quit()

if __name__ == "__main__":
    main()
