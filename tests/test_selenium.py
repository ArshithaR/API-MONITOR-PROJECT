import pytest

pytest.importorskip("selenium")

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from tests.conftest import run_test_server


@pytest.fixture
def browser():
    """Create a headless Chrome browser when available."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,1000")
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        pytest.skip(f"Chrome WebDriver not available: {exc}")
    yield driver
    driver.quit()


def test_home_page_login_and_register_links(app, browser):
    """Basic Selenium smoke test for landing page navigation."""
    with run_test_server(app) as live_url:
        browser.get(live_url)
        assert "API Monitor" in browser.title
        assert browser.find_element(By.LINK_TEXT, "Login").is_displayed()
        assert browser.find_element(By.LINK_TEXT, "Register").is_displayed()
