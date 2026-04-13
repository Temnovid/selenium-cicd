import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    """
    Setup for Chrome browser. 
    This configuration is optimized for WSL and CI/CD environments.
    """
    # 1. Initialize Chrome Options
    chrome_options = Options()
    
    # --- WSL & CI/CD ESSENTIAL FLAGS ---
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # AUTO-SWITCH: If running in GitHub Actions, force headless mode
    if os.environ.get('CI') == 'true':
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

    # --- TOGGLE HEADLESS MODE ---
    # Comment out the line below if you want to see the browser window (Headed)
    # Uncomment it for GitHub Actions or background execution (Headless)
    # chrome_options.add_argument("--headless") 

    # 2. Automatically install/update ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # 3. Start the browser session
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 4. Global wait (Wait up to 10 seconds for elements to appear)
    driver.implicitly_wait(10)
    
    # Return the driver to the test
    yield driver
    
    # 5. Teardown: Close the browser after the test completes
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This checks if a test failed
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if hasattr(item.config, 'slaveinput') else 'w'
        try:
            # Look for the 'driver' fixture in the test
            if 'driver' in item.fixturenames:
                web_driver = item.funcargs['driver']
                # Save a screenshot
                web_driver.save_screenshot(f"failure_{item.name}.png")
                print(f"\nScreenshot saved as failure_{item.name}.png")
        except Exception as e:
            print(f"Fail to take screenshot: {e}")
    