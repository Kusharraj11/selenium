import pytest
from login_page import LoginPage

# Test data: (username, password, should_succeed)
test_data = [
    ("tomsmith", "SuperSecretPassword!", True),
    ("tomsmith", "wrongpass", False),
    ("invalid_user", "invalid_pass", False),
]

@pytest.mark.parametrize("username,password,should_succeed", test_data)
def test_login_scenarios(driver, username, password, should_succeed):
    driver.get("https://the-internet.herokuapp.com/login")
    login_page = LoginPage(driver)
    login_page.login(username, password)

    if should_succeed:
        success_msg = login_page.get_success_message()
        assert "You logged into a secure area!" in success_msg
        print(f"✅ Login successful for: {username}")
    else:
        error_msg = login_page.get_error_message()
        assert "Your username is invalid!" in error_msg or "Your password is invalid!" in error_msg
        print(f"❌ Login failed as expected for: {username} - Message: {error_msg}")
