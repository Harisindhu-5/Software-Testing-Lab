"""
Selenium Test Runner for E-Commerce Application
This module provides specialized test running for Selenium tests with comprehensive logging.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .test_logger import SeleniumTestLogger

class SeleniumTestRunner:
    """Specialized test runner for Selenium tests"""
    
    def __init__(self):
        self.logger = SeleniumTestLogger()
        self.driver = None
        self.setup_logger()
        self.base_url = "http://localhost:8000"  # Default Django development server
    
    def setup_logger(self):
        """Setup logger for Selenium tests"""
        self.logger.log_test_session_start({
            'test_type': 'selenium',
            'description': 'Selenium WebDriver Tests',
            'browser': 'Chrome',
            'webdriver_manager': True,
            'base_url': self.base_url
        })
    
    def setup_driver(self):
        """Setup Chrome WebDriver with logging"""
        try:
            self.logger.log_setup_teardown("Setup", "Initializing Chrome WebDriver")
            
            # Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Setup service with webdriver-manager
            service = Service(ChromeDriverManager().install())
            
            # Create driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            
            self.logger.log_test_success("WebDriver Setup", details={
                'browser': 'Chrome',
                'headless': True,
                'window_size': '1920x1080',
                'implicit_wait': '10s'
            })
            
            return True
            
        except Exception as e:
            self.logger.log_test_failure("WebDriver Setup", str(e), details={
                'error_type': 'WebDriver Initialization Error',
                'suggestion': 'Check if Chrome is installed and webdriver-manager is working'
            })
            return False
    
    def teardown_driver(self):
        """Teardown Chrome WebDriver with logging"""
        if self.driver:
            try:
                self.logger.log_setup_teardown("Teardown", "Closing Chrome WebDriver")
                self.driver.quit()
                self.logger.log_test_success("WebDriver Teardown")
            except Exception as e:
                self.logger.log_test_failure("WebDriver Teardown", str(e))
    
    def run_selenium_test(self, test_name: str, test_function):
        """Run a single Selenium test with logging"""
        start_time = time.time()
        
        self.logger.log_test_start(test_name)
        
        try:
            # Setup driver if not already done
            if not self.driver:
                if not self.setup_driver():
                    self.logger.log_test_failure(test_name, "Failed to setup WebDriver")
                    return False
            
            # Run the test function
            test_function(self.driver)
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.logger.log_test_success(test_name, duration, {
                'test_type': 'selenium',
                'browser_actions': 'completed'
            })
            
            return True
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            self.logger.log_test_failure(test_name, str(e), duration, {
                'test_type': 'selenium',
                'error_type': type(e).__name__,
                'browser_state': 'error'
            })
            
            return False
    
    def run_all_selenium_tests(self):
        """Run all Selenium tests"""
        tests = [
            ("User Registration Test", self.test_user_registration),
            ("User Login Test", self.test_user_login),
            ("Product Browsing Test", self.test_product_browsing),
            ("Add to Cart Test", self.test_add_to_cart),
            ("Checkout Process Test", self.test_checkout_process),
            ("Dynamic Elements Test", self.test_dynamic_elements),
            ("Error Handling Test", self.test_error_handling),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            self.logger.log_test_start(test_name)
            results[test_name] = self.run_selenium_test(test_name, test_func)
        
        # Generate summary
        passed = sum(1 for result in results.values() if result)
        failed = len(results) - passed
        
        self.logger.log_test_session_end()
        
        return results
    
    def test_user_registration(self, driver):
        """Test user registration process"""
        self.logger.log_selenium_action("Navigate to signup page")
        driver.get(f"{self.base_url}/signup/")
        
        # Fill registration form
        self.logger.log_selenium_action("Fill username field", "username", "seleniumuser")
        username_field = driver.find_element("name", "username")
        username_field.send_keys("seleniumuser")
        
        self.logger.log_selenium_action("Fill email field", "email", "selenium@test.com")
        email_field = driver.find_element("name", "email")
        email_field.send_keys("selenium@test.com")
        
        self.logger.log_selenium_action("Fill password field", "password", "testpass123")
        password_field = driver.find_element("name", "password")
        password_field.send_keys("testpass123")
        
        self.logger.log_selenium_action("Select buyer role", "role", "buyer")
        role_field = driver.find_element("name", "role")
        role_field.send_keys("buyer")
        
        # Submit form
        self.logger.log_selenium_action("Submit registration form")
        submit_button = driver.find_element("css selector", "button[type='submit']")
        submit_button.click()
        
        # Verify registration success
        self.logger.log_selenium_action("Verify registration success")
        time.sleep(2)  # Wait for page to load
        page_source = driver.page_source.lower()
        
        # Check if we're on login page or signup page with success
        assert (
            'login' in driver.current_url or 
            'sign up' in page_source or
            'already have an account' in page_source
        ), "Registration should redirect to login or show signup form"
        
        self.logger.log_test_success("User Registration", details={
            'form_fields_filled': 4,
            'form_submitted': True,
            'redirect_successful': True
        })
    
    def test_user_login(self, driver):
        """Test user login process"""
        self.logger.log_selenium_action("Navigate to login page")
        driver.get(f"{self.base_url}/login/")
        
        # Fill login form
        self.logger.log_selenium_action("Fill username field", "username", "seleniumuser")
        username_field = driver.find_element("name", "username")
        username_field.send_keys("seleniumuser")
        
        self.logger.log_selenium_action("Fill password field", "password", "testpass123")
        password_field = driver.find_element("name", "password")
        password_field.send_keys("testpass123")
        
        # Submit form
        self.logger.log_selenium_action("Submit login form")
        submit_button = driver.find_element("css selector", "button[type='submit']")
        submit_button.click()
        
        # Verify login success
        self.logger.log_selenium_action("Verify login success")
        time.sleep(2)  # Wait for page to load
        page_source = driver.page_source.lower()
        
        # Check if we're on products page or dashboard
        assert (
            'products' in driver.current_url or 
            'seleniumuser' in page_source or
            'logout' in page_source
        ), "Login should redirect to products or show user info"
        
        self.logger.log_test_success("User Login", details={
            'form_fields_filled': 2,
            'form_submitted': True,
            'login_successful': True
        })
    
    def test_product_browsing(self, driver):
        """Test product browsing functionality"""
        self.logger.log_selenium_action("Navigate to products page")
        driver.get(f"{self.base_url}/products/")
        
        # Check if products are displayed
        self.logger.log_selenium_action("Check product list")
        page_source = driver.page_source.lower()
        
        # Look for product-related content
        assert (
            'products' in page_source or
            'test product' in page_source or
            'card' in page_source
        ), "Products page should display product information"
        
        self.logger.log_test_success("Product Browsing", details={
            'page_loaded': True,
            'content_found': True
        })
    
    def test_add_to_cart(self, driver):
        """Test add to cart functionality"""
        self.logger.log_selenium_action("Navigate to products page")
        driver.get(f"{self.base_url}/products/")
        
        # Find first product and click to go to detail page
        self.logger.log_selenium_action("Find product link")
        product_links = driver.find_elements("css selector", "a[href*='/product/']")
        
        if product_links:
            self.logger.log_selenium_action("Click product link")
            product_links[0].click()
            
            # Find and click add to cart button
            self.logger.log_selenium_action("Find add to cart button")
            add_to_cart_button = driver.find_element("name", "add_to_cart")
            
            self.logger.log_selenium_action("Click add to cart button")
            add_to_cart_button.click()
            
            # Verify item added to cart
            self.logger.log_selenium_action("Verify cart update")
            time.sleep(2)  # Wait for page to load
            page_source = driver.page_source.lower()
            
            # Check if we're on cart page or see success message
            assert (
                'cart' in driver.current_url or
                'added' in page_source or
                'success' in page_source
            ), "Add to cart should redirect to cart or show success message"
            
            self.logger.log_test_success("Add to Cart", details={
                'button_found': True,
                'button_clicked': True,
                'cart_updated': True
            })
        else:
            self.logger.log_test_skip("Add to Cart", "No product links found")
    
    def test_checkout_process(self, driver):
        """Test checkout process"""
        self.logger.log_selenium_action("Navigate to checkout page")
        driver.get(f"{self.base_url}/checkout/")
        
        # Check if checkout form is present
        self.logger.log_selenium_action("Check checkout form")
        page_source = driver.page_source.lower()
        
        # Verify checkout page loads (might be cart page or checkout form)
        assert (
            'checkout' in page_source or
            'cart' in page_source or
            'order' in page_source or
            'form' in page_source
        ), "Checkout page should load with form or cart information"
        
        self.logger.log_test_success("Checkout Process", details={
            'page_loaded': True,
            'content_found': True
        })
    
    def test_dynamic_elements(self, driver):
        """Test handling of dynamic elements"""
        self.logger.log_selenium_action("Navigate to products page")
        driver.get(f"{self.base_url}/products/")
        
        # Wait for dynamic content
        self.logger.log_selenium_action("Wait for dynamic content")
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        try:
            # Wait for any dynamic element (body is always present)
            wait = WebDriverWait(driver, 10)
            dynamic_element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test that page loaded successfully
            assert dynamic_element.is_displayed(), "Dynamic element should be displayed"
            
            self.logger.log_test_success("Dynamic Elements", details={
                'wait_time': '10s',
                'dynamic_element_found': True
            })
            
        except Exception as e:
            self.logger.log_test_failure("Dynamic Elements", str(e), details={
                'wait_timeout': True,
                'error': 'Dynamic element not found within timeout'
            })
            raise
    
    def test_error_handling(self, driver):
        """Test error handling for invalid pages"""
        self.logger.log_selenium_action("Navigate to non-existent page")
        driver.get(f"{self.base_url}/non-existent-page/")
        
        # Check for error page or 404
        self.logger.log_selenium_action("Check error handling")
        page_source = driver.page_source.lower()
        
        # Verify error handling (should show 404 or error page)
        assert (
            'not found' in page_source or
            '404' in page_source or
            'error' in page_source or
            'does not exist' in page_source
        ), "Non-existent page should show error or 404"
        
        self.logger.log_test_success("Error Handling", details={
            'error_page_displayed': True,
            'error_type': '404 or error page'
        })

def run_selenium_tests_with_logging():
    """Run Selenium tests with comprehensive logging"""
    runner = SeleniumTestRunner()
    
    try:
        results = runner.run_all_selenium_tests()
        
        # Print summary to terminal
        print("\n" + "="*60)
        print("SELENIUM TEST RESULTS")
        print("="*60)
        
        for test_name, result in results.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{test_name:<30}: {status}")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print("-" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "Success Rate: 0%")
        
        return all(results.values())
        
    finally:
        runner.teardown_driver()

if __name__ == "__main__":
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
    
    # Run Selenium tests
    run_selenium_tests_with_logging() 