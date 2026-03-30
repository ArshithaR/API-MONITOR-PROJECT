import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture
def driver():
    """Initialize Selenium WebDriver"""
    chrome_options = Options()
    # Uncomment for headless mode
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

class TestUIRegistrationLogin:
    """Test UI registration and login"""
    
    def test_register_new_user_ui(self, driver, app):
        """Test user registration through UI"""
        with app.app_context():
            driver.get("http://localhost:5000/register")
            
            # Fill registration form
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.send_keys("uiuser")
            password_field.send_keys("password123")
            
            # Submit form
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            
            # Verify registration
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            assert driver.current_url.endswith("/login")
    
    def test_login_user_ui(self, driver, app, auth_user):
        """Test user login through UI"""
        with app.app_context():
            driver.get("http://localhost:5000/login")
            
            # Fill login form
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            
            username_field.send_keys("testuser")
            password_field.send_keys("password123")
            
            # Submit form
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            
            # Verify login
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )
            assert "Dashboard" in driver.page_source

class TestUIDashboard:
    """Test dashboard UI interactions"""
    
    def test_add_api_through_ui(self, driver, app, auth_user):
        """Test adding API through UI"""
        with app.app_context():
            driver.get("http://localhost:5000/login")
            
            # Login
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            username_field.send_keys("testuser")
            password_field.send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "name"))
            )
            
            # Fill API form
            name_field = driver.find_element(By.NAME, "name")
            url_field = driver.find_element(By.NAME, "url")
            interval_field = driver.find_element(By.NAME, "interval")
            
            name_field.send_keys("Test UI API")
            url_field.send_keys("https://api.example.com")
            interval_field.clear()
            interval_field.send_keys("60")
            
            # Submit form
            submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Add API')]")
            submit_btn.click()
            
            # Verify API is added
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Test UI API')]"))
            )
    
    def test_view_analytics_button(self, driver, app, auth_user):
        """Test analytics button navigation"""
        with app.app_context():
            driver.get("http://localhost:5000/login")
            
            # Login
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            username_field.send_keys("testuser")
            password_field.send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Analytics')]"))
            )
            
            # Click analytics button
            analytics_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Analytics')]")
            analytics_btn.click()
            
            # Verify we're on analytics page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )
            assert "Performance Analytics" in driver.page_source

class TestUIChartInteraction:
    """Test chart interaction on UI"""
    
    def test_chart_type_selection(self, driver, app, auth_user, test_api):
        """Test selecting different chart types"""
        with app.app_context():
            driver.get("http://localhost:5000/login")
            
            # Login
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            username_field.send_keys("testuser")
            password_field.send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
            # Navigate to analytics
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Analytics')]"))
            )
            driver.find_element(By.XPATH, "//a[contains(text(), 'Analytics')]").click()
            
            # Select bar chart
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "barChart"))
            )
            bar_chart_radio = driver.find_element(By.ID, "barChart")
            bar_chart_radio.click()
            
            # Verify selection
            assert bar_chart_radio.is_selected()
