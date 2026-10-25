from selenium.webdriver.common.by import By

def test_history_page_opens(driver, base_url):
    driver.get(base_url + "/history")
    assert "Evidence history" in driver.page_source
