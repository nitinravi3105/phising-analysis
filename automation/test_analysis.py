
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException


def test_analyze_suspicious_message(driver, base_url):
    wait = WebDriverWait(driver, 15)
    driver.get(base_url)

    Select(
        wait.until(
            EC.presence_of_element_located((By.ID, "message_type"))
        )
    ).select_by_visible_text("SMS")

    message_box = wait.until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    message_box.send_keys(
        "URGENT: verify your password immediately "
        "at https://bit.ly/demo"
    )

    button = wait.until(
        EC.presence_of_element_located((By.ID, "analyze-button"))
    )

    driver.execute_script("""
        document.documentElement.style.scrollBehavior = 'auto';
        window.scrollTo(0, document.body.scrollHeight);
        arguments[0].scrollIntoView({block: 'center', inline: 'center'});
    """, button)

    try:
        wait.until(
            EC.element_to_be_clickable((By.ID, "analyze-button"))
        ).click()
    except ElementClickInterceptedException:
        # Fallback for viewport/layout interception.
        driver.execute_script(
            "arguments[0].form.requestSubmit();", button
        )

    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), "Analysis summary"
        )
    )

    assert "Evidence E-" in driver.page_source
    assert "High" in driver.page_source


def test_empty_message_native_validation(driver, base_url):
    driver.get(base_url)

    message_box = driver.find_element(By.ID, "message")
    assert message_box.get_attribute("required") is not None
