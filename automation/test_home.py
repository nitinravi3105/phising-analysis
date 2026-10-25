from selenium.webdriver.common.by import By

def test_home_page_loads(driver, base_url):
    driver.get(base_url)
    assert "PhishGuard Evidence Lab" in driver.title
    assert driver.find_element(By.ID, "message").is_displayed()
    assert driver.find_element(By.ID, "analyze-button").is_displayed()
