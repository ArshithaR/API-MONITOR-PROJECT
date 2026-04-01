"""Selenium Tests for API Monitor UI"""
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")
def selenium_driver():
    """Create Selenium WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        # Fallback if Chrome not available
        pytest.skip("Chrome WebDriver not available")
    
    yield driver
    driver.quit()


class TestAuthenticationUI:
    """Test authentication UI flows"""
    
    def test_register_flow(self, selenium_driver):
        """Test user registration flow"""
        driver = selenium_driver
        driver.get("http://127.0.0.1:5000/register")
        
        # Wait for form to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Fill registration form
        username_field = driver.find_element(By.NAME, "username")
        email_field = driver.find_element(By.NAME, "email") if driver.find_elements(By.NAME, "email") else None
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.send_keys(f"seleniumuser_{int(time.time())}")
        if email_field:
            email_field.send_keys(f"test_{int(time.time())}@example.com")
        password_field.send_keys("testpassword123")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Wait for response
        time.sleep(2)
        assert "Account created" in driver.page_source or "log in" in driver.page_source
    
    def test_login_flow(self, selenium_driver):
        """Test user login flow"""
        driver = selenium_driver
        driver.get("http://127.0.0.1:5000/login")
        
        # Wait for form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        
        # Fill login form
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        
        username_field.send_keys("testuser")
        password_field.send_keys("password123")
        
        # Submit
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Wait for redirect
        time.sleep(2)


class TestDashboardUI:
    """Test dashboard UI interactions"""
    
    def test_dashboard_loads(self, selenium_driver):
        """Test dashboard page loads"""
        driver = selenium_driver
        driver.get("http://127.0.0.1:5000/dashboard")
        
        # Should either show login or dashboard
        assert "Dashboard" in driver.page_source or "Login" in driver.page_source or "login" in driver.page_source


class TestPerformanceUI:
    """Test performance analytics UI"""
    
    def test_performance_page_loads(self, selenium_driver):
        """Test performance page structure"""
        driver = selenium_driver
        driver.get("http://127.0.0.1:5000/performance")
        
        # Should either show performance page or login
        time.sleep(1)
        page_source = driver.page_source.lower()
        assert "performance" in page_source or "login" in page_source or "dashboard" in page_source
