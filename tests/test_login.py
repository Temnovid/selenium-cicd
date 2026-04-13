from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_successful_login(driver):
    # 1. Open Site
    driver.get("https://www.saucedemo.com/")
    
    # 2. Initialize Page Objects
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    # 3. Perform Actions
    login_page.login_to_app("standard_user", "secret_sauce")
    
    # 4. Assertions (Verifying the result)
    assert "inventory.html" in driver.current_url
    assert inventory_page.get_title_text() == "Products"

def test_invalid_login(driver):
    driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(driver)
    
    login_page.login_to_app("locked_out_user", "secret_sauce")
    
    # Verify error message appears
    assert login_page.driver.find_element(*login_page.error_message).is_displayed()