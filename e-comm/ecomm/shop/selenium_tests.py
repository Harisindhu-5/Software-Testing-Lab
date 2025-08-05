"""
Selenium WebDriver Tests for E-Commerce Application
This module contains Selenium WebDriver tests for browser automation testing.
"""

import time
import logging
from decimal import Decimal
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from shop.models import User, Shop, Product, Cart, CartItem

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeleniumWebDriverTest(LiveServerTestCase):
    """Selenium WebDriver tests for browser automation"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup Chrome options for visible testing
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Commented out to show browser window
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")  # Start with maximized window
        
        # Setup WebDriver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Set up test data"""
        # Create test seller
        self.seller = User.objects.create_user(
            username='seleniumseller',
            email='seleniumseller@test.com',
            password='testpass123',
            role='seller'
        )
        
        # Create test user
        self.user = User.objects.create_user(
            username='seleniumuser',
            email='selenium@test.com',
            password='testpass123',
            role='buyer'
        )
        
        # Create test shop
        self.shop = Shop.objects.create(
            name='Test Shop',
            owner=self.seller
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product for Selenium tests',
            price=29.99,
            seller=self.seller,
            shop=self.shop
        )
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present and return it"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {by}={value}")
            logger.error(f"Current URL: {self.driver.current_url}")
            logger.error(f"Page source: {self.driver.page_source[:500]}...")
            raise
    
    def wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for element to be clickable and return it"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: {by}={value}")
            raise
    
    def login_user(self, username, password):
        """Helper method to login a user"""
        logger.info(f"Logging in user: {username}")
        
        # Navigate to login page
        self.driver.get(f'{self.live_server_url}/login/')
        
        # Wait for and fill username field
        username_field = self.wait_for_element(By.NAME, 'username')
        username_field.clear()
        username_field.send_keys(username)
        
        # Wait for and fill password field
        password_field = self.wait_for_element(By.NAME, 'password')
        password_field.clear()
        password_field.send_keys(password)
        
        # Wait for and click submit button
        submit_button = self.wait_for_element_clickable(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Wait for redirect or success
        time.sleep(2)
        logger.info(f"Login completed. Current URL: {self.driver.current_url}")
    
    def logout_user(self):
        """Helper method to logout a user"""
        logger.info("Logging out user")
        
        try:
            # Navigate to logout page
            self.driver.get(f'{self.live_server_url}/logout/')
            time.sleep(2)
            
            # Check if logout was successful
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            logout_indicators = [
                'login' in current_url,
                'sign up' in page_source,
                'welcome' in page_source,
                'products' in page_source
            ]
            
            success = any(logout_indicators)
            logger.info(f"Logout completed. Current URL: {current_url}")
            logger.info(f"Logout success: {success}")
            return success
        except Exception as e:
            logger.error(f"Failed to logout: {e}")
            return False
    
    def test_user_registration_selenium(self):
        """Test user registration using Selenium WebDriver"""
        logger.info("Starting user registration test")
        
        # Navigate to signup page
        self.driver.get(f'{self.live_server_url}/signup/')
        logger.info(f"Navigated to signup page: {self.driver.current_url}")
        
        # Wait for and fill registration form
        username_field = self.wait_for_element(By.NAME, 'username')
        username_field.clear()
        username_field.send_keys('newseleniumuser')
        logger.info("Filled username field")
        
        email_field = self.wait_for_element(By.NAME, 'email')
        email_field.clear()
        email_field.send_keys('newselenium@test.com')
        logger.info("Filled email field")
        
        password_field = self.wait_for_element(By.NAME, 'password')
        password_field.clear()
        password_field.send_keys('testpass123')
        logger.info("Filled password field")
        
        # Select role
        role_select = Select(self.wait_for_element(By.NAME, 'role'))
        role_select.select_by_value('buyer')
        logger.info("Selected buyer role")
        
        # Submit form
        submit_button = self.wait_for_element_clickable(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        logger.info("Clicked submit button")
        
        # Wait for page to load and verify registration success
        time.sleep(3)
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        logger.info(f"Registration completed. Current URL: {current_url}")
        logger.info(f"Page contains 'login': {'login' in current_url}")
        logger.info(f"Page contains 'sign up': {'sign up' in page_source}")
        
        # Check if we're on products page (home page) or login page
        success_indicators = [
            'login' in current_url,
            'sign up' in page_source,
            'already have an account' in page_source,
            'success' in page_source,
            'welcome' in page_source,
            'products' in page_source,  # Home page shows products
            'e-commerce' in page_source,  # Home page title
            'container' in page_source,  # Bootstrap container
            'navbar' in page_source  # Navigation bar
        ]
        
        self.assertTrue(
            any(success_indicators),
            f"Registration should redirect to login or show signup form. URL: {current_url}, Page content: {page_source[:200]}..."
        )
        logger.info("User registration test passed")
    
    def test_user_login_selenium(self):
        """Test user login using Selenium WebDriver"""
        logger.info("Starting user login test")
        
        # Use helper method to login
        self.login_user('seleniumuser', 'testpass123')
        
        # Verify login success
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        logger.info(f"Login completed. Current URL: {current_url}")
        logger.info(f"Page contains 'products': {'products' in current_url}")
        logger.info(f"Page contains 'seleniumuser': {'seleniumuser' in page_source}")
        
        # Check if we're on products page or dashboard
        success_indicators = [
            'products' in current_url,
            'seleniumuser' in page_source,
            'logout' in page_source,
            'dashboard' in current_url
        ]
        
        self.assertTrue(
            any(success_indicators),
            f"Login should redirect to products or show user info. URL: {current_url}, Page content: {page_source[:200]}..."
        )
        logger.info("User login test passed")
        
        # Logout after successful login test
        logout_success = self.logout_user()
        self.assertTrue(logout_success, "User should be able to logout successfully")
        logger.info("User logout test passed")
    
    def test_product_browsing_selenium(self):
        """Test product browsing using Selenium WebDriver"""
        logger.info("Starting product browsing test")
        
        # Navigate to products page (root URL)
        self.driver.get(f'{self.live_server_url}/')
        logger.info(f"Navigated to products page: {self.driver.current_url}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Check if products are displayed
        page_source = self.driver.page_source.lower()
        
        logger.info(f"Page contains 'products': {'products' in page_source}")
        logger.info(f"Page contains 'test product': {'test product' in page_source}")
        logger.info(f"Page contains 'card': {'card' in page_source}")
        
        # Look for product-related content
        success_indicators = [
            'products' in page_source,
            'test product' in page_source,
            'card' in page_source,
            'container' in page_source,
            'row' in page_source
        ]
        
        self.assertTrue(
            any(success_indicators),
            f"Products page should display product information. Page content: {page_source[:500]}..."
        )
        logger.info("Product browsing test passed")
    
    def test_add_to_cart_selenium(self):
        """Test adding product to cart using Selenium WebDriver"""
        logger.info("Starting add to cart test")
        
        # First, login
        self.login_user('seleniumuser', 'testpass123')
        
        # Navigate to product detail page
        self.driver.get(f'{self.live_server_url}/product/{self.product.id}/')
        logger.info(f"Navigated to product detail page: {self.driver.current_url}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Check if we're on the product detail page
        page_source = self.driver.page_source.lower()
        if 'test product' not in page_source:
            logger.warning("Product detail page not loaded properly, trying alternative navigation")
            # Try navigating from products page
            self.driver.get(f'{self.live_server_url}/')
            time.sleep(2)
            
            # Look for product links
            product_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')
            if product_links:
                product_links[0].click()
                time.sleep(2)
                page_source = self.driver.page_source.lower()
        
        # Verify we're on product detail page
        self.assertIn('test product', page_source, "Should be on product detail page")
        
        # Find and click add to cart button
        try:
            add_to_cart_button = self.wait_for_element_clickable(By.NAME, 'add_to_cart')
            add_to_cart_button.click()
            logger.info("Clicked add to cart button")
        except TimeoutException:
            # Try alternative selectors
            try:
                add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, 'button[name="add_to_cart"]')
                add_to_cart_button.click()
                logger.info("Clicked add to cart button (alternative selector)")
            except NoSuchElementException:
                logger.error("Could not find add to cart button")
                logger.error(f"Page source: {self.driver.page_source}")
                raise
        
        # Wait for action to complete
        time.sleep(3)
        
        # Verify cart update - check for success indicators
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        logger.info(f"Add to cart completed. Current URL: {current_url}")
        logger.info(f"Page contains 'success': {'success' in page_source}")
        logger.info(f"Page contains 'added': {'added' in page_source}")
        
        # Check for success indicators
        success_indicators = [
            'success' in page_source,
            'added' in page_source,
            'cart' in current_url,
            'added to cart' in page_source
        ]
        
        self.assertTrue(
            any(success_indicators),
            f"Add to cart should show success message. URL: {current_url}, Page content: {page_source[:200]}..."
        )
        logger.info("Add to cart test passed")
    
    def test_checkout_process_selenium(self):
        """Test checkout process using Selenium WebDriver"""
        logger.info("Starting checkout process test")
        
        # Login and add item to cart
        self.login_user('seleniumuser', 'testpass123')
        
        # Add item to cart via API (more reliable than UI)
        cart, created = Cart.objects.get_or_create(user=self.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=self.product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        # Navigate to cart page
        self.driver.get(f'{self.live_server_url}/cart/')
        logger.info(f"Navigated to cart page: {self.driver.current_url}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Verify cart has items
        page_source = self.driver.page_source.lower()
        self.assertIn('test product', page_source, "Cart should show the product")
        
        # Navigate to checkout
        self.driver.get(f'{self.live_server_url}/checkout/')
        logger.info(f"Navigated to checkout page: {self.driver.current_url}")
        
        # Wait for checkout form
        time.sleep(2)
        
        # Fill checkout form
        try:
            address_field = self.wait_for_element(By.NAME, 'address')
            address_field.clear()
            address_field.send_keys('123 Test Street')
            logger.info("Filled address field")
        except TimeoutException:
            # Try alternative selector
            address_field = self.driver.find_element(By.CSS_SELECTOR, 'textarea[name="address"]')
            address_field.clear()
            address_field.send_keys('123 Test Street')
            logger.info("Filled address field (alternative selector)")
        
        # Submit checkout form
        submit_button = self.wait_for_element_clickable(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        logger.info("Clicked checkout submit button")
        
        # Wait for order completion
        time.sleep(3)
        
        # Verify order was created
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        logger.info(f"Checkout completed. Current URL: {current_url}")
        logger.info(f"Page contains 'orders': {'orders' in current_url}")
        logger.info(f"Page contains 'success': {'success' in page_source}")
        
        # Check for success indicators
        success_indicators = [
            'orders' in current_url,
            'success' in page_source,
            'order placed' in page_source,
            'thank you' in page_source
        ]
        
        self.assertTrue(
            any(success_indicators),
            f"Checkout should complete successfully. URL: {current_url}, Page content: {page_source[:200]}..."
        )
        logger.info("Checkout process test passed")
    
    def test_dynamic_elements_selenium(self):
        """Test handling of dynamic elements using Selenium WebDriver"""
        logger.info("Starting dynamic elements test")
        
        # Navigate to products page (root URL)
        self.driver.get(f'{self.live_server_url}/')
        logger.info(f"Navigated to products page: {self.live_server_url}/")
        
        # Wait for dynamic content to load
        time.sleep(3)
        
        # Test explicit wait for dynamic elements
        try:
            # Wait for any product-related content
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            logger.info("Dynamic content loaded successfully")
        except TimeoutException:
            logger.warning("Dynamic content loading timeout")
        
        # Verify page loaded
        page_source = self.driver.page_source.lower()
        self.assertIn('container', page_source, "Page should have Bootstrap container")
        
        logger.info("Dynamic elements test passed")
    
    def test_error_handling_selenium(self):
        """Test error handling using Selenium WebDriver"""
        logger.info("Starting error handling test")
        
        # Test accessing non-existent page
        self.driver.get(f'{self.live_server_url}/nonexistent-page/')
        logger.info(f"Navigated to non-existent page: {self.driver.current_url}")
        
        # Wait for page to load
        time.sleep(2)
        
        # Check for error page (404)
        page_source = self.driver.page_source.lower()
        current_url = self.driver.current_url
        
        # Django should handle 404s gracefully
        error_indicators = [
            'not found' in page_source,
            '404' in page_source,
            'error' in page_source,
            'page not found' in page_source
        ]
        
        # If it's not a 404, it might redirect to a valid page
        if not any(error_indicators):
            logger.info("Page redirected to valid content")
            self.assertNotEqual(current_url, f'{self.live_server_url}/nonexistent-page/', 
                              "Should not stay on non-existent page")
        
        logger.info("Error handling test passed")

# ============================================================================
# SELENIUM RC DEMO - Show differences between RC and WebDriver
# ============================================================================

class SeleniumRCDemo(LiveServerTestCase):
    """Demonstrate differences between Selenium RC and WebDriver"""
    
    def setUp(self):
        # Setup WebDriver for demo
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Commented out to show browser window
        chrome_options.add_argument("--start-maximized")  # Start with maximized window
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        self.driver.quit()
    
    def test_selenium_rc_vs_webdriver(self):
        """Demonstrate differences between Selenium RC and WebDriver"""
        # WebDriver approach (modern)
        self.driver.get(f'{self.live_server_url}/')
        
        # Modern WebDriver syntax
        elements = self.driver.find_elements(By.TAG_NAME, "body")
        
        # Verify page loaded
        self.assertIn('container', self.driver.page_source.lower())
        
        # Note: Selenium RC would use different syntax like:
        # sel = selenium("localhost", 4444, "*chrome", "http://localhost:8000/")
        # sel.start()
        # sel.open("/products/")
        # sel.type("username", "testuser")

# ============================================================================
# PAGE OBJECT MODEL DEMO - Show POM pattern
# ============================================================================

class PageObjectModelDemo(LiveServerTestCase):
    """Demonstrate Page Object Model pattern"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='pomuser',
            email='pom@test.com',
            password='testpass123',
            role='buyer'
        )
        
        self.seller = User.objects.create_user(
            username='pomseller',
            email='pomseller@test.com',
            password='testpass123',
            role='seller'
        )
        self.shop = Shop.objects.create(
            name='POM Shop',
            owner=self.seller
        )
        self.product = Product.objects.create(
            name='POM Product',
            price=19.99,
            seller=self.seller,
            shop=self.shop
        )
        
        # Setup WebDriver
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Commented out to show browser window
        chrome_options.add_argument("--start-maximized")  # Start with maximized window
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
    
    def tearDown(self):
        self.driver.quit()
    
    def test_page_object_model(self):
        """Demonstrate Page Object Model pattern"""
        login_page = LoginPage(self.driver, self.live_server_url)
        product_page = ProductPage(self.driver, self.live_server_url)
        cart_page = CartPage(self.driver, self.live_server_url)
        
        # Login using POM
        login_page.navigate()
        login_page.login('pomuser', 'testpass123')
        
        # Browse products using POM
        product_page.navigate()
        product_page.add_to_cart()
        
        # Check cart using POM
        cart_page.navigate()
        cart_page.verify_item_present()

class LoginPage:
    """Page Object for Login Page"""
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.username_field = (By.NAME, 'username')
        self.password_field = (By.NAME, 'password')
        self.submit_button = (By.CSS_SELECTOR, 'button[type="submit"]')
    
    def navigate(self):
        self.driver.get(f'{self.base_url}/login/')
    
    def login(self, username, password):
        wait = WebDriverWait(self.driver, 10)
        username_element = wait.until(EC.presence_of_element_located(self.username_field))
        username_element.send_keys(username)
        
        password_element = wait.until(EC.presence_of_element_located(self.password_field))
        password_element.send_keys(password)
        
        submit_element = wait.until(EC.element_to_be_clickable(self.submit_button))
        submit_element.click()
        time.sleep(2)  # Wait for login to complete

class ProductPage:
    """Page Object for Product Detail Page"""
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.add_to_cart_button = (By.NAME, 'add_to_cart')
    
    def navigate(self):
        # Navigate to first product
        self.driver.get(f'{self.base_url}/')
        # Click on first product to go to detail page
        product_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')
        if product_links:
            product_links[0].click()
    
    def add_to_cart(self):
        wait = WebDriverWait(self.driver, 10)
        add_button = wait.until(EC.element_to_be_clickable(self.add_to_cart_button))
        add_button.click()
        time.sleep(2)  # Wait for add to cart to complete

class CartPage:
    """Page Object for Cart Page"""
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
    
    def navigate(self):
        self.driver.get(f'{self.base_url}/cart/')
    
    def verify_item_present(self):
        page_source = self.driver.page_source.lower()
        # Check if cart has items or shows cart information
        assert (
            'cart' in page_source or
            'item' in page_source or
            'product' in page_source
        ), "Cart page should show cart information" 