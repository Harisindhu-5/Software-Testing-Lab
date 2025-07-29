from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
import time
import json

from .models import (
    User, Shop, Product, Cart, CartItem, 
    Wishlist, WishlistItem, Order, OrderItem
)

# ============================================================================
# UNIT TESTS - Testing Individual Components
# ============================================================================

class UserModelTest(TestCase):
    """Unit tests for User model"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        }
    
    def test_user_creation(self):
        """Test basic user creation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'buyer')
        self.assertTrue(user.is_active)
    
    def test_user_role_validation(self):
        """Test user role validation"""
        user = User.objects.create_user(**self.user_data)
        user.role = 'invalid_role'
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')

class ProductModelTest(TestCase):
    """Unit tests for Product model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.shop = Shop.objects.create(
            name="Test Shop",
            owner=self.user
        )
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': Decimal('29.99'),
            'image': 'https://example.com/image.jpg',
            'seller': self.user,
            'shop': self.shop
        }
    
    def test_product_creation(self):
        """Test basic product creation"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.price, Decimal('29.99'))
        self.assertEqual(product.seller, self.user)
    
    def test_product_price_validation(self):
        """Test product price validation"""
        # Test negative price
        self.product_data['price'] = Decimal('-10.00')
        with self.assertRaises(ValidationError):
            product = Product(**self.product_data)
            product.full_clean()
    
    def test_product_string_representation(self):
        """Test product string representation"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(str(product), 'Test Product')

class CartModelTest(TestCase):
    """Unit tests for Cart model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_cart_creation(self):
        """Test cart creation for user"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
    
    def test_cart_item_creation(self):
        """Test adding items to cart"""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.product, self.product)
    
    def test_cart_total_calculation(self):
        """Test cart total calculation"""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        total = sum(item.product.price * item.quantity for item in cart.items.all())
        self.assertEqual(total, Decimal('59.98'))

class OrderModelTest(TestCase):
    """Unit tests for Order model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_order_creation(self):
        """Test order creation"""
        order = Order.objects.create(
            user=self.user,
            address='123 Test Street',
            status='Pending'
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'Pending')
    
    def test_order_item_creation(self):
        """Test order item creation"""
        order = Order.objects.create(
            user=self.user,
            address='123 Test Street'
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=3,
            price=self.product.price
        )
        self.assertEqual(order_item.quantity, 3)
        self.assertEqual(order_item.price, self.product.price)

# ============================================================================
# INTEGRATION TESTS - Testing Component Interactions
# ============================================================================

class CartIntegrationTest(TestCase):
    """Integration tests for cart functionality"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_add_to_cart_workflow(self):
        """Test complete add to cart workflow"""
        # Login user
        self.client.login(username='buyer', password='testpass123')
        
        # Add product to cart
        response = self.client.post(
            reverse('product_detail', args=[self.product.id]),
            {'add_to_cart': 'true'}
        )
        
        # Check cart was created and item added
        cart = Cart.objects.get(user=self.buyer)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)
    
    def test_cart_quantity_update(self):
        """Test cart quantity update functionality"""
        self.client.login(username='buyer', password='testpass123')
        
        # Add product to cart
        self.client.post(
            reverse('product_detail', args=[self.product.id]),
            {'add_to_cart': 'true'}
        )
        
        # Update quantity
        cart = Cart.objects.get(user=self.buyer)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        
        response = self.client.post(reverse('cart'), {
            f'quantity_{cart_item.id}': '3'
        })
        
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

class OrderIntegrationTest(TestCase):
    """Integration tests for order functionality"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_checkout_workflow(self):
        """Test complete checkout workflow"""
        self.client.login(username='buyer', password='testpass123')
        
        # Add product to cart
        self.client.post(
            reverse('product_detail', args=[self.product.id]),
            {'add_to_cart': 'true'}
        )
        
        # Checkout
        response = self.client.post(reverse('checkout'), {
            'address': '123 Test Street'
        })
        
        # Verify order was created
        order = Order.objects.get(user=self.buyer)
        self.assertEqual(order.address, '123 Test Street')
        self.assertEqual(order.status, 'Pending')
        
        # Verify order item was created
        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 1)

# ============================================================================
# FUNCTIONAL TESTS - Testing Complete User Workflows
# ============================================================================

class UserWorkflowTest(TestCase):
    """Functional tests for complete user workflows"""
    
    def setUp(self):
        self.client = Client()
    
    def test_buyer_registration_and_purchase_workflow(self):
        """Test complete buyer registration and purchase workflow"""
        # 1. Register as buyer
        response = self.client.post(reverse('signup'), {
            'username': 'newbuyer',
            'email': 'newbuyer@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after signup
        
        # 2. Login
        response = self.client.post(reverse('login'), {
            'username': 'newbuyer',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # 3. Create a seller and product
        seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=seller
        )
        
        # 4. Add to cart
        response = self.client.post(
            reverse('product_detail', args=[product.id]),
            {'add_to_cart': 'true'}
        )
        self.assertEqual(response.status_code, 302)
        
        # 5. Checkout
        response = self.client.post(reverse('checkout'), {
            'address': '123 Test Street'
        })
        self.assertEqual(response.status_code, 302)
        
        # 6. Verify order was created
        user = User.objects.get(username='newbuyer')
        order = Order.objects.get(user=user)
        self.assertEqual(order.address, '123 Test Street')
    
    def test_seller_registration_and_product_management_workflow(self):
        """Test complete seller registration and product management workflow"""
        # 1. Register as seller
        response = self.client.post(reverse('signup'), {
            'username': 'newseller',
            'email': 'newseller@example.com',
            'password': 'testpass123',
            'role': 'seller'
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Login
        response = self.client.post(reverse('login'), {
            'username': 'newseller',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # 3. Create product
        response = self.client.post(reverse('product_create'), {
            'name': 'New Product',
            'description': 'New Description',
            'price': '39.99',
            'image': 'https://example.com/image.jpg'
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. Verify product was created
        user = User.objects.get(username='newseller')
        product = Product.objects.get(seller=user)
        self.assertEqual(product.name, 'New Product')
        self.assertEqual(product.price, Decimal('39.99'))

# ============================================================================
# EDGE CASE TESTS - Testing Boundary Conditions and Error Scenarios
# ============================================================================

class EdgeCaseTest(TestCase):
    """Tests for edge cases and error scenarios"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_duplicate_username_registration(self):
        """Test registration with duplicate username"""
        # Create first user
        User.objects.create_user(
            username='testuser',
            email='test1@example.com',
            password='testpass123',
            role='buyer'
        )
        
        # Try to create second user with same username
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test2@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        })
        
        # Should not redirect (stay on signup page)
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_login_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        })
        
        # Should not redirect (stay on login page)
        self.assertEqual(response.status_code, 200)
    
    def test_access_restricted_pages_without_login(self):
        """Test accessing restricted pages without login"""
        # Try to access cart without login
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Try to access seller dashboard without login
        response = self.client.get(reverse('seller_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_seller_accessing_buyer_features(self):
        """Test seller trying to access buyer-specific features"""
        self.client.login(username='seller', password='testpass123')
        
        # Seller should be redirected from buyer features
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)  # Can view products
    
    def test_buyer_accessing_seller_features(self):
        """Test buyer trying to access seller-specific features"""
        self.client.login(username='buyer', password='testpass123')
        
        # Buyer should be redirected from seller features
        response = self.client.get(reverse('seller_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to product list
    
    def test_empty_cart_checkout(self):
        """Test checkout with empty cart"""
        self.client.login(username='buyer', password='testpass123')
        
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to cart
    
    def test_product_with_zero_price(self):
        """Test product creation with zero price"""
        self.client.login(username='seller', password='testpass123')
        
        response = self.client.post(reverse('product_create'), {
            'name': 'Free Product',
            'description': 'Free Description',
            'price': '0.00',
            'image': 'https://example.com/image.jpg'
        })
        
        # Should work (zero price is valid)
        self.assertEqual(response.status_code, 302)
    
    def test_product_with_negative_price(self):
        """Test product creation with negative price"""
        self.client.login(username='seller', password='testpass123')
        
        response = self.client.post(reverse('product_create'), {
            'name': 'Negative Product',
            'description': 'Negative Description',
            'price': '-10.00',
            'image': 'https://example.com/image.jpg'
        })
        
        # Should fail validation
        self.assertEqual(response.status_code, 200)  # Stay on form page

# ============================================================================
# PERFORMANCE TESTS - Testing Application Performance
# ============================================================================

class PerformanceTest(TestCase):
    """Performance tests for the application"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        
        # Create multiple products for performance testing
        for i in range(50):
            Product.objects.create(
                name=f'Product {i}',
                description=f'Description {i}',
                price=Decimal(f'{i}.99'),
                seller=self.seller
            )
    
    def test_product_list_performance(self):
        """Test product list page performance"""
        start_time = time.time()
        response = self.client.get(reverse('product_list'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        # Response should be under 1 second
        self.assertLess(end_time - start_time, 1.0)
    
    def test_database_query_optimization(self):
        """Test that database queries are optimized"""
        from django.db import connection
        
        # Clear connection queries
        connection.queries = []
        
        # Access product list
        self.client.get(reverse('product_list'))
        
        # Check number of queries (should be minimal)
        query_count = len(connection.queries)
        self.assertLess(query_count, 10)  # Should be optimized
    
    def test_large_cart_performance(self):
        """Test performance with large cart"""
        self.client.login(username='buyer', password='testpass123')
        
        # Add many items to cart
        products = Product.objects.all()[:20]
        for product in products:
            self.client.post(
                reverse('product_detail', args=[product.id]),
                {'add_to_cart': 'true'}
            )
        
        # Test cart page performance
        start_time = time.time()
        response = self.client.get(reverse('cart'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0)

# ============================================================================
# SECURITY TESTS - Testing Authentication and Authorization
# ============================================================================

class SecurityTest(TestCase):
    """Security tests for authentication and authorization"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        # Try to submit form without CSRF token
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        })
        
        # Should fail due to CSRF protection
        self.assertEqual(response.status_code, 403)
    
    def test_authentication_required_pages(self):
        """Test that protected pages require authentication"""
        protected_urls = [
            reverse('cart'),
            reverse('wishlist'),
            reverse('orders'),
            reverse('seller_dashboard'),
            reverse('checkout'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_authorization_based_on_user_role(self):
        """Test authorization based on user roles"""
        # Buyer should not access seller dashboard
        self.client.login(username='buyer', password='testpass123')
        response = self.client.get(reverse('seller_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # Seller should access seller dashboard
        self.client.login(username='seller', password='testpass123')
        response = self.client.get(reverse('seller_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_product_ownership_validation(self):
        """Test that sellers can only edit their own products"""
        other_seller = User.objects.create_user(
            username='otherseller',
            email='other@example.com',
            password='testpass123',
            role='seller'
        )
        other_product = Product.objects.create(
            name='Other Product',
            description='Other Description',
            price=Decimal('19.99'),
            seller=other_seller
        )
        
        # Try to edit other seller's product
        self.client.login(username='seller', password='testpass123')
        response = self.client.get(reverse('product_edit', args=[other_product.id]))
        self.assertEqual(response.status_code, 404)  # Not found
    
    def test_session_management(self):
        """Test session management and logout"""
        self.client.login(username='buyer', password='testpass123')
        
        # Should be able to access protected pages
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        
        # Logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        
        # Should not be able to access protected pages after logout
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

# ============================================================================
# API TESTS - Testing URL Patterns and Response Formats
# ============================================================================

class APITest(TestCase):
    """Tests for URL patterns and response formats"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_url_patterns(self):
        """Test all URL patterns are accessible"""
        urls_to_test = [
            ('product_list', []),
            ('product_detail', [self.product.id]),
            ('signup', []),
            ('login', []),
        ]
        
        for url_name, args in urls_to_test:
            response = self.client.get(reverse(url_name, args=args))
            self.assertIn(response.status_code, [200, 302])  # 200 for success, 302 for redirect
    
    def test_response_content_types(self):
        """Test response content types"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
    
    def test_template_rendering(self):
        """Test that templates render correctly"""
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'Products')
        self.assertContains(response, 'Sort by Name')
    
    def test_form_submission(self):
        """Test form submission and validation"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        })
        
        # Should redirect after successful signup
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        user = User.objects.get(username='newuser')
        self.assertEqual(user.role, 'buyer')

# ============================================================================
# DATA VALIDATION TESTS - Testing Data Integrity
# ============================================================================

class DataValidationTest(TestCase):
    """Tests for data validation and integrity"""
    
    def setUp(self):
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
    
    def test_product_price_validation(self):
        """Test product price validation"""
        # Valid price
        product = Product(
            name='Valid Product',
            description='Valid Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
        product.full_clean()  # Should not raise exception
        
        # Invalid price (negative)
        product.price = Decimal('-10.00')
        with self.assertRaises(ValidationError):
            product.full_clean()
    
    def test_user_email_validation(self):
        """Test user email validation"""
        # Valid email
        user = User(
            username='testuser',
            email='valid@example.com',
            role='buyer'
        )
        user.full_clean()  # Should not raise exception
        
        # Invalid email
        user.email = 'invalid-email'
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    def test_unique_constraints(self):
        """Test unique constraints"""
        # Create first user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='buyer'
        )
        
        # Try to create second user with same username
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username='testuser',
                email='test2@example.com',
                password='testpass123',
                role='buyer'
            )

# ============================================================================
# CONCURRENCY TESTS - Testing Race Conditions
# ============================================================================

class ConcurrencyTest(TestCase):
    """Tests for race conditions and concurrency issues"""
    
    def setUp(self):
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_concurrent_cart_operations(self):
        """Test concurrent cart operations"""
        from threading import Thread
        import time
        
        def add_to_cart():
            client = Client()
            client.login(username='buyer', password='testpass123')
            client.post(
                reverse('product_detail', args=[self.product.id]),
                {'add_to_cart': 'true'}
            )
        
        # Start multiple threads
        threads = []
        for _ in range(5):
            thread = Thread(target=add_to_cart)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify cart integrity
        cart = Cart.objects.get(user=self.buyer)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        # Should have 5 items (one from each thread)
        self.assertEqual(cart_item.quantity, 5)

# ============================================================================
# ERROR HANDLING TESTS - Testing Error Scenarios
# ============================================================================

class ErrorHandlingTest(TestCase):
    """Tests for error handling and edge cases"""
    
    def setUp(self):
        self.client = Client()
    
    def test_nonexistent_product_access(self):
        """Test accessing non-existent product"""
        response = self.client.get(reverse('product_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_url_patterns(self):
        """Test invalid URL patterns"""
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)
    
    def test_malformed_form_data(self):
        """Test form submission with malformed data"""
        response = self.client.post(reverse('signup'), {
            'username': '',  # Empty username
            'email': 'invalid-email',
            'password': '',  # Empty password
            'role': 'invalid-role'
        })
        
        # Should stay on form page (not redirect)
        self.assertEqual(response.status_code, 200)
    
    def test_database_constraint_violations(self):
        """Test database constraint violations"""
        # Try to create product without required fields
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='',  # Empty name
                price=Decimal('29.99')
                # Missing seller
            )

# ============================================================================
# USABILITY TESTS - Testing User Experience
# ============================================================================

class UsabilityTest(TestCase):
    """Tests for user experience and usability"""
    
    def setUp(self):
        self.client = Client()
        self.buyer = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123',
            role='buyer'
        )
        self.seller = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123',
            role='seller'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('29.99'),
            seller=self.seller
        )
    
    def test_navigation_consistency(self):
        """Test navigation consistency across pages"""
        # Check that navigation elements are present on all pages
        pages = [
            reverse('product_list'),
            reverse('login'),
            reverse('signup'),
        ]
        
        for page in pages:
            response = self.client.get(page)
            self.assertContains(response, 'E-Commerce')  # Brand name
            self.assertContains(response, 'Login')  # Login link
    
    def test_form_validation_messages(self):
        """Test form validation messages"""
        response = self.client.post(reverse('signup'), {
            'username': '',  # Empty username
            'email': 'invalid-email',
            'password': '',  # Empty password
            'role': 'buyer'
        })
        
        # Should show validation errors
        self.assertEqual(response.status_code, 200)
    
    def test_success_messages(self):
        """Test success messages after actions"""
        self.client.login(username='buyer', password='testpass123')
        
        # Add to cart
        response = self.client.post(
            reverse('product_detail', args=[self.product.id]),
            {'add_to_cart': 'true'}
        )
        
        # Should redirect (success)
        self.assertEqual(response.status_code, 302)
    
    def test_responsive_design_elements(self):
        """Test responsive design elements"""
        response = self.client.get(reverse('product_list'))
        
        # Check for Bootstrap classes (responsive design)
        self.assertContains(response, 'container')
        self.assertContains(response, 'row')
        self.assertContains(response, 'col-md-4')

# ============================================================================
# COMPREHENSIVE TEST SUITE RUNNER
# ============================================================================

class ComprehensiveTestSuite(TestCase):
    """Comprehensive test suite that runs all major functionality"""
    
    def setUp(self):
        self.client = Client()
    
    def test_complete_ecommerce_workflow(self):
        """Test complete e-commerce workflow from registration to purchase"""
        # 1. Register buyer
        response = self.client.post(reverse('signup'), {
            'username': 'comprehensive_buyer',
            'email': 'comprehensive@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        })
        self.assertEqual(response.status_code, 302)
        
        # 2. Register seller
        response = self.client.post(reverse('signup'), {
            'username': 'comprehensive_seller',
            'email': 'comprehensive_seller@example.com',
            'password': 'testpass123',
            'role': 'seller'
        })
        self.assertEqual(response.status_code, 302)
        
        # 3. Login as seller and create product
        self.client.login(username='comprehensive_seller', password='testpass123')
        response = self.client.post(reverse('product_create'), {
            'name': 'Comprehensive Test Product',
            'description': 'Comprehensive Test Description',
            'price': '49.99',
            'image': 'https://example.com/comprehensive.jpg'
        })
        self.assertEqual(response.status_code, 302)
        
        # 4. Login as buyer
        self.client.login(username='comprehensive_buyer', password='testpass123')
        
        # 5. Browse products
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        
        # 6. Add to cart
        product = Product.objects.get(name='Comprehensive Test Product')
        response = self.client.post(
            reverse('product_detail', args=[product.id]),
            {'add_to_cart': 'true'}
        )
        self.assertEqual(response.status_code, 302)
        
        # 7. View cart
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        
        # 8. Checkout
        response = self.client.post(reverse('checkout'), {
            'address': '123 Comprehensive Street'
        })
        self.assertEqual(response.status_code, 302)
        
        # 9. View orders
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        
        # 10. Verify order was created
        buyer = User.objects.get(username='comprehensive_buyer')
        order = Order.objects.get(user=buyer)
        self.assertEqual(order.address, '123 Comprehensive Street')
        self.assertEqual(order.status, 'Pending')
