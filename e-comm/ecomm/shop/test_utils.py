"""
Test utilities for the e-commerce application.
This module provides helper functions and test data generators for comprehensive testing.
"""

import random
import string
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import User, Shop, Product, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem

User = get_user_model()

class TestDataGenerator:
    """Utility class for generating test data"""
    
    @staticmethod
    def generate_random_string(length=10):
        """Generate a random string of specified length"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_random_email():
        """Generate a random email address"""
        username = TestDataGenerator.generate_random_string(8)
        domain = TestDataGenerator.generate_random_string(5)
        return f"{username}@{domain}.com"
    
    @staticmethod
    def generate_random_price():
        """Generate a random price between 1.00 and 1000.00"""
        return Decimal(str(random.uniform(1.00, 1000.00)).split('.')[0] + '.' + str(random.randint(10, 99)))
    
    @staticmethod
    def create_test_user(role='buyer', **kwargs):
        """Create a test user with default or custom attributes"""
        username = kwargs.get('username', f'testuser_{TestDataGenerator.generate_random_string(5)}')
        email = kwargs.get('email', TestDataGenerator.generate_random_email())
        password = kwargs.get('password', 'testpass123')
        
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            **kwargs
        )
    
    @staticmethod
    def create_test_seller(**kwargs):
        """Create a test seller with shop"""
        seller = TestDataGenerator.create_test_user(role='seller', **kwargs)
        shop_name = kwargs.get('shop_name', f"{seller.username}'s Shop")
        Shop.objects.create(name=shop_name, owner=seller)
        return seller
    
    @staticmethod
    def create_test_product(seller=None, **kwargs):
        """Create a test product with default or custom attributes"""
        if seller is None:
            seller = TestDataGenerator.create_test_seller()
        
        name = kwargs.get('name', f'Test Product {TestDataGenerator.generate_random_string(5)}')
        description = kwargs.get('description', f'Test Description {TestDataGenerator.generate_random_string(20)}')
        price = kwargs.get('price', TestDataGenerator.generate_random_price())
        image = kwargs.get('image', 'https://via.placeholder.com/150')
        
        return Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image,
            seller=seller,
            shop=seller.shop
        )
    
    @staticmethod
    def create_test_cart(user):
        """Create a test cart for a user"""
        return Cart.objects.get_or_create(user=user)[0]
    
    @staticmethod
    def create_test_cart_item(cart, product, quantity=1):
        """Create a test cart item"""
        return CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )
    
    @staticmethod
    def create_test_wishlist(user):
        """Create a test wishlist for a user"""
        return Wishlist.objects.get_or_create(user=user)[0]
    
    @staticmethod
    def create_test_wishlist_item(wishlist, product):
        """Create a test wishlist item"""
        return WishlistItem.objects.create(
            wishlist=wishlist,
            product=product
        )
    
    @staticmethod
    def create_test_order(user, address="123 Test Street", status="Pending"):
        """Create a test order"""
        return Order.objects.create(
            user=user,
            address=address,
            status=status
        )
    
    @staticmethod
    def create_test_order_item(order, product, quantity=1):
        """Create a test order item"""
        return OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
    
    @staticmethod
    def create_bulk_test_data(num_users=10, num_products=50, num_orders=20):
        """Create bulk test data for performance testing"""
        # Create users
        buyers = []
        sellers = []
        
        for i in range(num_users // 2):
            buyer = TestDataGenerator.create_test_user(role='buyer')
            buyers.append(buyer)
        
        for i in range(num_users // 2):
            seller = TestDataGenerator.create_test_seller()
            sellers.append(seller)
        
        # Create products
        products = []
        for seller in sellers:
            for i in range(num_products // len(sellers)):
                product = TestDataGenerator.create_test_product(seller)
                products.append(product)
        
        # Create orders
        orders = []
        for buyer in buyers:
            for i in range(num_orders // len(buyers)):
                order = TestDataGenerator.create_test_order(buyer)
                # Add random products to order
                order_products = random.sample(products, min(3, len(products)))
                for product in order_products:
                    TestDataGenerator.create_test_order_item(
                        order, product, random.randint(1, 5)
                    )
                orders.append(order)
        
        return {
            'buyers': buyers,
            'sellers': sellers,
            'products': products,
            'orders': orders
        }

class TestAssertions:
    """Custom assertions for testing"""
    
    @staticmethod
    def assert_valid_user(test_case, user, expected_role=None):
        """Assert that a user is valid"""
        test_case.assertIsNotNone(user)
        test_case.assertTrue(user.is_active)
        test_case.assertIsNotNone(user.username)
        test_case.assertIsNotNone(user.email)
        if expected_role:
            test_case.assertEqual(user.role, expected_role)
    
    @staticmethod
    def assert_valid_product(test_case, product, expected_seller=None):
        """Assert that a product is valid"""
        test_case.assertIsNotNone(product)
        test_case.assertIsNotNone(product.name)
        test_case.assertIsNotNone(product.description)
        test_case.assertGreater(product.price, 0)
        test_case.assertIsNotNone(product.seller)
        if expected_seller:
            test_case.assertEqual(product.seller, expected_seller)
    
    @staticmethod
    def assert_valid_order(test_case, order, expected_user=None):
        """Assert that an order is valid"""
        test_case.assertIsNotNone(order)
        test_case.assertIsNotNone(order.user)
        test_case.assertIsNotNone(order.address)
        test_case.assertIsNotNone(order.status)
        if expected_user:
            test_case.assertEqual(order.user, expected_user)
    
    @staticmethod
    def assert_cart_integrity(test_case, cart):
        """Assert cart data integrity"""
        test_case.assertIsNotNone(cart)
        test_case.assertIsNotNone(cart.user)
        
        # Check that all cart items have valid products
        for item in cart.items.all():
            test_case.assertIsNotNone(item.product)
            test_case.assertGreater(item.quantity, 0)
    
    @staticmethod
    def assert_order_integrity(test_case, order):
        """Assert order data integrity"""
        test_case.assertIsNotNone(order)
        test_case.assertIsNotNone(order.user)
        test_case.assertIsNotNone(order.address)
        
        # Check that all order items have valid products and prices
        for item in order.items.all():
            test_case.assertIsNotNone(item.product)
            test_case.assertGreater(item.quantity, 0)
            test_case.assertGreater(item.price, 0)

class PerformanceTestHelper:
    """Helper class for performance testing"""
    
    @staticmethod
    def measure_response_time(test_case, url, method='get', data=None):
        """Measure response time for a URL"""
        import time
        
        start_time = time.time()
        if method.lower() == 'get':
            response = test_case.client.get(url)
        else:
            response = test_case.client.post(url, data)
        end_time = time.time()
        
        return {
            'response': response,
            'response_time': end_time - start_time,
            'status_code': response.status_code
        }
    
    @staticmethod
    def measure_database_queries(test_case, func, *args, **kwargs):
        """Measure number of database queries for a function"""
        from django.db import connection
        
        # Clear connection queries
        connection.queries = []
        
        # Execute function
        result = func(*args, **kwargs)
        
        # Count queries
        query_count = len(connection.queries)
        
        return {
            'result': result,
            'query_count': query_count,
            'queries': connection.queries
        }
    
    @staticmethod
    def benchmark_function(test_case, func, iterations=100, *args, **kwargs):
        """Benchmark a function over multiple iterations"""
        import time
        
        times = []
        for _ in range(iterations):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            times.append(end_time - start_time)
        
        return {
            'result': result,
            'times': times,
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times)
        }

class SecurityTestHelper:
    """Helper class for security testing"""
    
    @staticmethod
    def test_csrf_protection(test_case, url, data):
        """Test CSRF protection on a URL"""
        # Test without CSRF token
        response = test_case.client.post(url, data)
        return response.status_code == 403
    
    @staticmethod
    def test_authentication_required(test_case, url):
        """Test that a URL requires authentication"""
        response = test_case.client.get(url)
        return response.status_code == 302  # Redirect to login
    
    @staticmethod
    def test_authorization_required(test_case, url, user, expected_status=200):
        """Test that a URL requires proper authorization"""
        test_case.client.login(username=user.username, password='testpass123')
        response = test_case.client.get(url)
        return response.status_code == expected_status
    
    @staticmethod
    def test_session_management(test_case, user):
        """Test session management"""
        # Login
        test_case.client.login(username=user.username, password='testpass123')
        
        # Test access to protected page
        response = test_case.client.get('/cart/')
        test_case.assertEqual(response.status_code, 200)
        
        # Logout
        response = test_case.client.get('/logout/')
        test_case.assertEqual(response.status_code, 302)
        
        # Test access denied after logout
        response = test_case.client.get('/cart/')
        test_case.assertEqual(response.status_code, 302)

class TestDataCleanup:
    """Helper class for cleaning up test data"""
    
    @staticmethod
    def cleanup_test_data():
        """Clean up all test data"""
        User.objects.all().delete()
        Shop.objects.all().delete()
        Product.objects.all().delete()
        Cart.objects.all().delete()
        CartItem.objects.all().delete()
        Wishlist.objects.all().delete()
        WishlistItem.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
    
    @staticmethod
    def cleanup_user_data(username_pattern='testuser_'):
        """Clean up test data for specific users"""
        User.objects.filter(username__startswith=username_pattern).delete()
    
    @staticmethod
    def cleanup_product_data(name_pattern='Test Product'):
        """Clean up test data for specific products"""
        Product.objects.filter(name__startswith=name_pattern).delete()

# Test configuration constants
class TestConfig:
    """Configuration constants for testing"""
    
    # Performance thresholds
    MAX_RESPONSE_TIME = 1.0  # seconds
    MAX_DATABASE_QUERIES = 10
    
    # Test data sizes
    SMALL_DATASET = 10
    MEDIUM_DATASET = 50
    LARGE_DATASET = 100
    
    # Security test constants
    VALID_ROLES = ['buyer', 'seller']
    INVALID_ROLES = ['admin', 'moderator', 'invalid']
    
    # Test user credentials
    TEST_USERNAME = 'testuser'
    TEST_PASSWORD = 'testpass123'
    TEST_EMAIL = 'test@example.com'
    
    # Test product data
    TEST_PRODUCT_NAME = 'Test Product'
    TEST_PRODUCT_DESCRIPTION = 'Test Description'
    TEST_PRODUCT_PRICE = Decimal('29.99')
    TEST_PRODUCT_IMAGE = 'https://via.placeholder.com/150'
    
    # Test order data
    TEST_ORDER_ADDRESS = '123 Test Street'
    TEST_ORDER_STATUS = 'Pending'
    
    # Error messages
    ERROR_MESSAGES = {
        'duplicate_username': 'Username already exists.',
        'invalid_credentials': 'Invalid username or password.',
        'empty_cart': 'Your cart is empty.',
        'access_denied': 'Access denied.',
        'not_found': 'Not found.',
    } 