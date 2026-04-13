from selenium.webdriver.common.by import By

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.title_label = (By.CLASS_NAME, "title")
        self.inventory_list = (By.CLASS_NAME, "inventory_list")

    def get_title_text(self):
        return self.driver.find_element(*self.title_label).text