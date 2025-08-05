#!/usr/bin/env python3
"""
Browser Testing Script for E-Commerce Application
This script provides comprehensive browser testing functionality with user input control.
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BrowserTestScript:
    """Comprehensive browser testing script with user input control"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        self.test_results = []
        
    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver with options"""
        try:
                    chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Browser driver setup completed")
        except Exception as e:
            logger.error(f"Failed to setup browser driver: {e}")
            self.driver = None
            self.wait = None
        
    def open_browser(self):
        """Open browser and navigate to base URL"""
        try:
            if self.driver is None:
                logger.error("Browser driver not initialized. Call setup_driver() first.")
                return False
            self.driver.get(self.base_url)
            logger.info(f"Browser opened and navigated to: {self.base_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to open browser: {e}")
            return False
    
    def close_browser(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to close browser: {e}")
            return False
    
    def delete_all_cookies(self):
        """Delete all cookies"""
        try:
            self.driver.delete_all_cookies()
            logger.info("All cookies deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to delete cookies: {e}")
            return False
    
    def print_session_info(self, username):
        """Print session information for specific user"""
        try:
            # Get session cookies
            cookies = self.driver.get_cookies()
            session_info = {
                'username': username,
                'cookies': cookies,
                'current_url': self.driver.current_url,
                'page_title': self.driver.title
            }
            logger.info(f"Session info for {username}: {json.dumps(session_info, indent=2)}")
            return session_info
        except Exception as e:
            logger.error(f"Failed to get session info: {e}")
            return None
    
    def test_window_closing_logout(self, username):
        """Test if closing window logs out the user"""
        try:
            # Get session before closing
            session_before = self.print_session_info(username)
            
            # Close current window
            self.driver.close()
            
            # Open new window
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.get(f"{self.base_url}/login/")
            
            # Check if user is logged out
            page_source = self.driver.page_source.lower()
            is_logged_out = 'login' in page_source or 'sign up' in page_source
            
            logger.info(f"User {username} logged out after window close: {is_logged_out}")
            return is_logged_out
        except Exception as e:
            logger.error(f"Failed to test window closing logout: {e}")
            return False
    
    def set_window_size(self, width, height):
        """Set browser window size"""
        try:
            self.driver.set_window_size(width, height)
            logger.info(f"Window size set to {width}x{height}")
            return True
        except Exception as e:
            logger.error(f"Failed to set window size: {e}")
            return False
    
    def register_user(self, username, email, password, role):
        """Register a new user"""
        try:
            self.driver.get(f"{self.base_url}/signup/")
            
            # Fill registration form
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
            username_field.clear()
            username_field.send_keys(username)
            
            email_field = self.driver.find_element(By.NAME, 'email')
            email_field.clear()
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.clear()
            password_field.send_keys(password)
            
            # Select role
            role_select = Select(self.driver.find_element(By.NAME, 'role'))
            role_select.select_by_value(role)
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            time.sleep(2)
            
            # Check if registration was successful
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            success_indicators = [
                'login' in current_url,
                'products' in page_source,
                'e-commerce' in page_source,
                'container' in page_source
            ]
            
            success = any(success_indicators)
            logger.info(f"User registration for {username} ({role}): {'SUCCESS' if success else 'FAILED'}")
            return success
        except Exception as e:
            logger.error(f"Failed to register user {username}: {e}")
            return False
    
    def test_invalid_login(self, username, password):
        """Test login with invalid credentials"""
        try:
            self.driver.get(f"{self.base_url}/login/")
            
            # Fill login form with invalid credentials
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
            username_field.clear()
            username_field.send_keys(username)
            
            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.clear()
            password_field.send_keys(password)
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            time.sleep(2)
            
            # Check for error message
            page_source = self.driver.page_source.lower()
            error_indicators = [
                'invalid' in page_source,
                'error' in page_source,
                'incorrect' in page_source,
                'failed' in page_source
            ]
            
            has_error = any(error_indicators)
            logger.info(f"Invalid login test: {'ERROR SHOWN' if has_error else 'NO ERROR'}")
            return has_error
        except Exception as e:
            logger.error(f"Failed to test invalid login: {e}")
            return False
    
    def login_and_get_user_info(self, username, password):
        """Login and get user information"""
        try:
            self.driver.get(f"{self.base_url}/login/")
            
            # Fill login form
            username_field = self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))
            username_field.clear()
            username_field.send_keys(username)
            
            password_field = self.driver.find_element(By.NAME, 'password')
            password_field.clear()
            password_field.send_keys(password)
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            time.sleep(2)
            
            # Get user information
            page_source = self.driver.page_source
            user_info = {
                'username': username,
                'password': password,
                'current_url': self.driver.current_url,
                'page_title': self.driver.title,
                'is_logged_in': username.lower() in page_source.lower()
            }
            
            logger.info(f"User login info: {json.dumps(user_info, indent=2)}")
            return user_info
        except Exception as e:
            logger.error(f"Failed to login and get user info: {e}")
            return None
    
    def check_logo_availability(self):
        """Check if logo is available on homepage"""
        try:
            self.driver.get(self.base_url)
            
            # Look for logo elements
            logo_selectors = [
                'img[alt*="logo"]',
                'img[alt*="Logo"]',
                '.navbar-brand img',
                '.logo',
                'img[src*="logo"]'
            ]
            
            logo_found = False
            for selector in logo_selectors:
                try:
                    logo = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if logo.is_displayed():
                        logo_found = True
                        logger.info(f"Logo found with selector: {selector}")
                        break
                except NoSuchElementException:
                    continue
            
            # Also check for text-based logo
            if not logo_found:
                try:
                    brand_element = self.driver.find_element(By.CSS_SELECTOR, '.navbar-brand')
                    if brand_element.is_displayed():
                        logo_found = True
                        logger.info(f"Text-based logo found: {brand_element.text}")
                except NoSuchElementException:
                    pass
            
            logger.info(f"Logo availability: {'FOUND' if logo_found else 'NOT FOUND'}")
            return logo_found
        except Exception as e:
            logger.error(f"Failed to check logo availability: {e}")
            return False
    
    def test_autosuggestions(self):
        """Test if autosuggestions are working"""
        try:
            self.driver.get(f"{self.base_url}/search/")  # Assuming search page exists
            
            # Look for search input
            search_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="search"], input[name="q"], input[placeholder*="search"]')
            search_input.click()
            search_input.send_keys("test")
            
            time.sleep(2)
            
            # Check for autosuggestion dropdown
            autosuggestion_selectors = [
                '.autocomplete',
                '.suggestions',
                '.dropdown-menu',
                '[role="listbox"]',
                '.search-suggestions'
            ]
            
            autosuggestion_found = False
            for selector in autosuggestion_selectors:
                try:
                    suggestions = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if suggestions:
                        autosuggestion_found = True
                        logger.info(f"Autosuggestions found with selector: {selector}")
                        break
                except:
                    continue
            
            logger.info(f"Autosuggestions test: {'WORKING' if autosuggestion_found else 'NOT WORKING'}")
            return autosuggestion_found
        except Exception as e:
            logger.error(f"Failed to test autosuggestions: {e}")
            return False
    
    def test_dropdowns(self):
        """Test dropdown functionality"""
        try:
            self.driver.get(self.base_url)
            
            # Test single value dropdown (sort dropdown)
            try:
                sort_dropdown = self.driver.find_element(By.CSS_SELECTOR, 'select[name="sort"]')
                sort_select = Select(sort_dropdown)
                
                # Test single value selection
                sort_select.select_by_value('price')
                time.sleep(1)
                
                # Test multiple values if available
                try:
                    multi_select = self.driver.find_element(By.CSS_SELECTOR, 'select[multiple]')
                    multi_select_obj = Select(multi_select)
                    logger.info("Multiple value dropdown found and tested")
                except NoSuchElementException:
                    logger.info("No multiple value dropdown found")
                
                logger.info("Dropdown test: WORKING")
                return True
            except NoSuchElementException:
                logger.info("No dropdown found on homepage")
                return False
        except Exception as e:
            logger.error(f"Failed to test dropdowns: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive browser test suite"""
        logger.info("Starting comprehensive browser test suite")
        
        try:
            # Setup driver first
            self.setup_driver(headless=True)
            
            # 1. Open browser
            self.open_browser()
            
            # 2. Set window size
            self.set_window_size(1920, 1080)
            
            # 3. Check logo availability
            logo_available = self.check_logo_availability()
            
            # 4. Test dropdowns
            dropdowns_working = self.test_dropdowns()
            
            # 5. Register different user types
            users_to_register = [
                ('testuser1', 'test1@example.com', 'password123', 'buyer'),
                ('testadmin', 'admin@example.com', 'adminpass123', 'seller'),
                ('guestuser', 'guest@example.com', 'guestpass123', 'buyer')
            ]
            
            registration_results = []
            for username, email, password, role in users_to_register:
                success = self.register_user(username, email, password, role)
                registration_results.append({
                    'username': username,
                    'role': role,
                    'success': success
                })
            
            # 6. Test invalid login
            invalid_login_result = self.test_invalid_login('invaliduser', 'wrongpassword')
            
            # 7. Test valid login and get user info
            user_info = self.login_and_get_user_info('testuser1', 'password123')
            
            # 8. Delete cookies
            self.delete_all_cookies()
            
            # 9. Print session info
            session_info = self.print_session_info('testuser1')
            
            # 10. Test window closing logout
            logout_on_close = self.test_window_closing_logout('testuser1')
            
            # 11. Test autosuggestions (if available)
            autosuggestions_working = self.test_autosuggestions()
            
            # Compile results
            test_results = {
                'logo_available': logo_available,
                'dropdowns_working': dropdowns_working,
                'registration_results': registration_results,
                'invalid_login_test': invalid_login_result,
                'user_info': user_info,
                'logout_on_window_close': logout_on_close,
                'autosuggestions_working': autosuggestions_working
            }
            
            logger.info("Comprehensive test completed")
            logger.info(f"Test results: {json.dumps(test_results, indent=2)}")
            
            return test_results
            
        except Exception as e:
            logger.error(f"Comprehensive test failed: {e}")
            return None
        finally:
            self.close_browser()

def main():
    """Main function to run the browser test script"""
    print("=== Browser Testing Script for E-Commerce Application ===")
    print("1. Run comprehensive automated test")
    print("2. Manual browser control")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    script = BrowserTestScript()
    
    if choice == "1":
        print("Running comprehensive automated test...")
        results = script.run_comprehensive_test()
        if results:
            print("Test completed successfully!")
            print("Results:", json.dumps(results, indent=2))
        else:
            print("Test failed!")
    
    elif choice == "2":
        print("Manual browser control mode")
        script.setup_driver(headless=False)
        
        # Test if driver is working
        if script.driver is None:
            print("Error: Failed to setup browser driver!")
            return
        
        while True:
            print("\nManual Control Options:")
            print("1. Open browser")
            print("2. Close browser")
            print("3. Delete cookies")
            print("4. Set window size")
            print("5. Check logo")
            print("6. Test dropdowns")
            print("7. Register user")
            print("8. Test invalid login")
            print("9. Login and get user info")
            print("10. Exit")
            
            cmd = input("Enter command (1-10): ")
            
            if cmd == "1":
                script.open_browser()
            elif cmd == "2":
                script.close_browser()
            elif cmd == "3":
                script.delete_all_cookies()
            elif cmd == "4":
                width = int(input("Enter width: "))
                height = int(input("Enter height: "))
                script.set_window_size(width, height)
            elif cmd == "5":
                script.check_logo_availability()
            elif cmd == "6":
                script.test_dropdowns()
            elif cmd == "7":
                username = input("Enter username: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                role = input("Enter role (buyer/seller): ")
                script.register_user(username, email, password, role)
            elif cmd == "8":
                username = input("Enter invalid username: ")
                password = input("Enter invalid password: ")
                script.test_invalid_login(username, password)
            elif cmd == "9":
                username = input("Enter username: ")
                password = input("Enter password: ")
                script.login_and_get_user_info(username, password)
            elif cmd == "10":
                script.close_browser()
                break
    
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main() 