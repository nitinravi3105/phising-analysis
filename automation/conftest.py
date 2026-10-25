import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def base_url():
    return os.environ.get("APP_BASE_URL", "http://127.0.0.1:5000")

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1365,900")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()
