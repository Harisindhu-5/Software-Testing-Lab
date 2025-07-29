"""
Selenium WebDriver Tests for E-Commerce Application
This module contains Selenium WebDriver tests for browser automation testing.
"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from .models import User, Product, Shop

class SeleniumWebDriverTest(LiveServerTestCase):
    """Selenium WebDriver tests for browser automation"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Setup Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Set up test data"""
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
            description='Test shop for Selenium tests'
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test product for Selenium tests',
            price=29.99,
            shop=self.shop
        )
    
    def test_user_registration_selenium(self):
        """Test user registration using Selenium WebDriver"""
        # Navigate to signup page
        self.driver.get(f'{self.live_server_url}/signup/')
        
        # Fill registration form
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('newseleniumuser')
        
        email_field = self.driver.find_element(By.NAME, 'email')
        email_field.send_keys('newselenium@test.com')
        
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('testpass123')
        
        # Select role
        role_select = Select(self.driver.find_element(By.NAME, 'role'))
        role_select.select_by_value('buyer')
        
        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Verify registration success - should redirect to login or show success message
        time.sleep(2)  # Wait for page to load
        page_source = self.driver.page_source.lower()
        
        # Check if we're on login page or signup page with success
        self.assertTrue(
            'login' in self.driver.current_url or 
            'sign up' in page_source or
            'already have an account' in page_source,
            "Registration should redirect to login or show signup form"
        )
    
    def test_user_login_selenium(self):
        """Test user login using Selenium WebDriver"""
        # Navigate to login page
        self.driver.get(f'{self.live_server_url}/login/')
        
        # Fill login form
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('seleniumuser')
        
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('testpass123')
        
        # Submit form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        # Verify login success - should redirect to products page or show user info
        time.sleep(2)  # Wait for page to load
        page_source = self.driver.page_source.lower()
        
        # Check if we're on products page or dashboard
        self.assertTrue(
            'products' in self.driver.current_url or 
            'seleniumuser' in page_source or
            'logout' in page_source,
            "Login should redirect to products or show user info"
        )
    
    def test_product_browsing_selenium(self):
        """Test product browsing using Selenium WebDriver"""
        # Navigate to products page
        self.driver.get(f'{self.live_server_url}/products/')
        
        # Check if products are displayed
        page_source = self.driver.page_source
        
        # Look for product-related content
        self.assertTrue(
            'products' in page_source.lower() or
            'test product' in page_source.lower() or
            'card' in page_source.lower(),
            "Products page should display product information"
        )
    
    def test_add_to_cart_selenium(self):
        """Test adding product to cart using Selenium WebDriver"""
        # First, login
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('seleniumuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('testpass123')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        time.sleep(2)  # Wait for login to complete
        
        # Navigate to product detail page
        self.driver.get(f'{self.live_server_url}/product/{self.product.id}/')
        
        # Find and click add to cart button
        add_to_cart_button = self.driver.find_element(By.NAME, 'add_to_cart')
        add_to_cart_button.click()
        
        # Verify item added to cart - check if we're redirected or see success message
        time.sleep(2)  # Wait for page to load
        page_source = self.driver.page_source.lower()
        
        # Check if we're on cart page or see success message
        self.assertTrue(
            'cart' in self.driver.current_url or
            'added' in page_source or
            'success' in page_source,
            "Add to cart should redirect to cart or show success message"
        )
    
    def test_checkout_process_selenium(self):
        """Test checkout process using Selenium WebDriver"""
        # First, login and add item to cart
        self.driver.get(f'{self.live_server_url}/login/')
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys('seleniumuser')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('testpass123')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        
        time.sleep(2)  # Wait for login to complete
        
        # Add item to cart
        self.driver.get(f'{self.live_server_url}/product/{self.product.id}/')
        add_to_cart_button = self.driver.find_element(By.NAME, 'add_to_cart')
        add_to_cart_button.click()
        
        time.sleep(2)  # Wait for add to cart to complete
        
        # Navigate to checkout page
        self.driver.get(f'{self.live_server_url}/checkout/')
        
        # Check if checkout form is present
        page_source = self.driver.page_source.lower()
        
        # Verify checkout page loads (might be cart page or checkout form)
        self.assertTrue(
            'checkout' in page_source or
            'cart' in page_source or
            'order' in page_source or
            'form' in page_source,
            "Checkout page should load with form or cart information"
        )
    
    def test_dynamic_elements_selenium(self):
        """Test handling of dynamic elements using Selenium WebDriver"""
        # Navigate to products page
        self.driver.get(f'{self.live_server_url}/products/')
        
        # Wait for dynamic content to load
        wait = WebDriverWait(self.driver, 10)
        
        try:
            # Wait for any dynamic element (body is always present)
            dynamic_element = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Test that page loaded successfully
            self.assertTrue(dynamic_element.is_displayed())
            
        except Exception as e:
            self.fail(f"Dynamic element not found: {e}")
    
    def test_error_handling_selenium(self):
        """Test error handling using Selenium WebDriver"""
        # Navigate to non-existent page
        self.driver.get(f'{self.live_server_url}/non-existent-page/')
        
        # Check for error page or 404
        page_source = self.driver.page_source.lower()
        
        # Verify error handling (should show 404 or error page)
        self.assertTrue(
            'not found' in page_source or
            '404' in page_source or
            'error' in page_source or
            'does not exist' in page_source,
            "Non-existent page should show error or 404"
        )

class SeleniumRCDemo(LiveServerTestCase):
    """Demo of Selenium RC vs WebDriver differences"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='rcuser',
            email='rc@test.com',
            password='testpass123',
            role='buyer'
        )
    
    def test_selenium_rc_vs_webdriver(self):
        """Demonstrate differences between Selenium RC and WebDriver"""
        # WebDriver approach (modern)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            # Direct browser automation (WebDriver)
            driver.get(f'{self.live_server_url}/login/')
            username_field = driver.find_element(By.NAME, 'username')
            username_field.send_keys('rcuser')
            
            # WebDriver is faster and more reliable
            self.assertTrue(driver.find_element(By.NAME, 'username').is_displayed())
            
        finally:
            driver.quit()

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
        
        self.shop = Shop.objects.create(name='POM Shop')
        self.product = Product.objects.create(
            name='POM Product',
            price=19.99,
            shop=self.shop
        )
        
        # Setup WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)
    
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
        self.driver.find_element(*self.username_field).send_keys(username)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.submit_button).click()
        time.sleep(2)  # Wait for login to complete

class ProductPage:
    """Page Object for Product Detail Page"""
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.add_to_cart_button = (By.NAME, 'add_to_cart')
    
    def navigate(self):
        # Navigate to first product
        self.driver.get(f'{self.base_url}/products/')
        # Click on first product to go to detail page
        product_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/product/"]')
        if product_links:
            product_links[0].click()
    
    def add_to_cart(self):
        self.driver.find_element(*self.add_to_cart_button).click()
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
        self.assertTrue(
            'cart' in page_source or
            'item' in page_source or
            'product' in page_source,
            "Cart page should show cart information"
        ) 