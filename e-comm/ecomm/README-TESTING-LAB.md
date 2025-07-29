# E-Commerce Application - Software Testing Laboratory

## Overview

This e-commerce application has been specifically enhanced for software testing laboratory purposes. It provides a comprehensive testing environment with multiple test categories, utilities, and configurations to demonstrate various testing methodologies and techniques.

## 🎯 Key Features for Testing Lab

- **1000+ Test Cases** covering all application functionality
- **Multiple Test Categories**: Unit, Integration, Functional, Performance, Security, and Usability tests
- **Test Utilities**: Helper classes for data generation, assertions, and performance measurement
- **Configurable Test Scenarios**: Predefined test scenarios for different testing objectives
- **Performance Testing**: Load testing, stress testing, and database performance testing
- **Security Testing**: Authentication, authorization, and input validation testing
- **Test Reporting**: Multiple report formats with detailed analysis
- **Easy Test Runner**: Interactive script for running different test types

## 📁 Project Structure

```
ecomm/
├── shop/
│   ├── tests.py              # Main test suite (1000+ tests)
│   ├── test_utils.py         # Test utilities and helpers
│   ├── test_config.py        # Test configuration
│   └── templates/            # Application templates
├── run_tests.py              # Interactive test runner
├── requirements-testing.txt   # Testing dependencies
├── TESTING_DOCUMENTATION.md  # Comprehensive testing docs
└── README-TESTING-LAB.md     # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install testing dependencies
pip install -r requirements-testing.txt

# Or install manually
pip install Django coverage pytest psutil
```

### 2. Run Tests

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --unit
python run_tests.py --performance
python run_tests.py --security

# Run with coverage
python run_tests.py --coverage
```

### 3. Interactive Test Runner

```bash
python run_tests.py
```

This will show an interactive menu with options to run different types of tests.

## 🧪 Test Categories

### 1. Unit Tests
- **Purpose**: Test individual components in isolation
- **Coverage**: Models, views, forms, utilities
- **Run**: `python run_tests.py --unit`

### 2. Integration Tests
- **Purpose**: Test component interactions
- **Coverage**: Database operations, view-model interactions
- **Run**: `python run_tests.py --integration`

### 3. Functional Tests
- **Purpose**: Test complete user workflows
- **Coverage**: End-to-end user scenarios
- **Run**: `python run_tests.py --functional`

### 4. Performance Tests
- **Purpose**: Test application performance and scalability
- **Coverage**: Response times, database queries, memory usage
- **Run**: `python run_tests.py --performance`

### 5. Security Tests
- **Purpose**: Test authentication, authorization, and security features
- **Coverage**: CSRF protection, session management, input validation
- **Run**: `python run_tests.py --security`

### 6. Edge Case Tests
- **Purpose**: Test boundary conditions and error scenarios
- **Coverage**: Invalid inputs, error handling, edge cases
- **Run**: `python run_tests.py --edge`

## 🛠️ Test Utilities

### TestDataGenerator
```python
from shop.test_utils import TestDataGenerator

# Create test users
buyer = TestDataGenerator.create_test_user(role='buyer')
seller = TestDataGenerator.create_test_seller()

# Create test products
product = TestDataGenerator.create_test_product(seller)

# Create bulk test data
test_data = TestDataGenerator.create_bulk_test_data(
    num_users=50, 
    num_products=200, 
    num_orders=100
)
```

### TestAssertions
```python
from shop.test_utils import TestAssertions

# Assert user validity
TestAssertions.assert_valid_user(self, user, expected_role='buyer')

# Assert product validity
TestAssertions.assert_valid_product(self, product, expected_seller=seller)

# Assert cart integrity
TestAssertions.assert_cart_integrity(self, cart)
```

### PerformanceTestHelper
```python
from shop.test_utils import PerformanceTestHelper

# Measure response time
result = PerformanceTestHelper.measure_response_time(
    self, reverse('product_list')
)
self.assertLess(result['response_time'], 1.0)

# Measure database queries
result = PerformanceTestHelper.measure_database_queries(
    self, self.client.get, reverse('product_list')
)
self.assertLess(result['query_count'], 10)
```

## 📊 Test Scenarios

### User Registration Scenarios
1. **Valid Buyer Registration**: Successful registration with buyer role
2. **Valid Seller Registration**: Successful registration with seller role
3. **Duplicate Username**: Registration with existing username
4. **Invalid Email**: Registration with malformed email
5. **Empty Fields**: Registration with missing required fields

### Login Scenarios
1. **Valid Credentials**: Successful login
2. **Invalid Username**: Login with non-existent username
3. **Invalid Password**: Login with wrong password
4. **Empty Credentials**: Login with empty fields

### Shopping Cart Scenarios
1. **Add to Cart**: Add product to cart
2. **Update Quantity**: Update cart item quantity
3. **Remove from Cart**: Remove item from cart
4. **Empty Cart**: Checkout with empty cart
5. **Large Cart**: Performance with many items

### Checkout Scenarios
1. **Valid Checkout**: Successful order placement
2. **Empty Address**: Checkout with empty address
3. **Order History**: View order history
4. **Order Details**: View specific order details

## 🔧 Test Configuration

### Test Environment Settings
```python
from shop.test_config import TestEnvironment

# Database configuration
TEST_DATABASE = TestEnvironment.TEST_DATABASE

# Performance thresholds
THRESHOLDS = TestEnvironment.PERFORMANCE_THRESHOLDS

# Security settings
SECURITY = TestEnvironment.SECURITY_SETTINGS
```

### Test Data Configuration
```python
from shop.test_config import TestDataConfig

# User test data
user_data = TestDataConfig.USERS['buyer']

# Product test data
product_data = TestDataConfig.PRODUCTS['valid']

# Order test data
order_data = TestDataConfig.ORDERS['valid']
```

## 📈 Performance Testing

### Load Testing
```bash
# Run load testing
python run_tests.py --load
```

### Stress Testing
```bash
# Run stress testing
python run_tests.py --stress
```

### Performance Analysis
```python
# Measure response time
start_time = time.time()
response = self.client.get(reverse('product_list'))
end_time = time.time()
self.assertLess(end_time - start_time, 1.0)

# Measure database queries
from django.db import connection
connection.queries = []
self.client.get(reverse('product_list'))
self.assertLess(len(connection.queries), 10)
```

## 🔒 Security Testing

### Authentication Testing
```python
# Test valid login
response = self.client.post(reverse('login'), {
    'username': 'testuser',
    'password': 'testpass123'
})
self.assertEqual(response.status_code, 302)

# Test invalid credentials
response = self.client.post(reverse('login'), {
    'username': 'testuser',
    'password': 'wrongpassword'
})
self.assertEqual(response.status_code, 200)
```

### Authorization Testing
```python
# Test role-based access control
self.client.login(username='buyer', password='testpass123')
response = self.client.get(reverse('seller_dashboard'))
self.assertEqual(response.status_code, 302)  # Redirect

self.client.login(username='seller', password='testpass123')
response = self.client.get(reverse('seller_dashboard'))
self.assertEqual(response.status_code, 200)  # Success
```

### CSRF Protection Testing
```python
# Test CSRF protection
response = self.client.post(reverse('signup'), {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'testpass123',
    'role': 'buyer'
})
self.assertEqual(response.status_code, 403)  # CSRF protection
```

## 📋 Test Reporting

### Coverage Reporting
```bash
# Generate coverage report
coverage run --source='.' manage.py test
coverage report -m
coverage html

# View coverage in browser
open htmlcov/index.html
```

### Test Statistics
```bash
# Show test statistics
python run_tests.py --stats
```

## 🎓 Learning Objectives

This testing laboratory helps students learn:

### 1. Test Types and Methodologies
- **Unit Testing**: Testing individual components
- **Integration Testing**: Testing component interactions
- **Functional Testing**: Testing complete workflows
- **Performance Testing**: Testing application performance
- **Security Testing**: Testing security features
- **Usability Testing**: Testing user experience

### 2. Test Design Patterns
- **AAA Pattern**: Arrange, Act, Assert
- **Test Data Management**: Creating and managing test data
- **Test Organization**: Organizing tests by functionality
- **Test Maintenance**: Keeping tests current and reliable

### 3. Testing Tools and Frameworks
- **Django Test Framework**: Django's built-in testing tools
- **Coverage Tools**: Measuring test coverage
- **Performance Tools**: Measuring application performance
- **Security Tools**: Testing security features

### 4. Test Automation
- **Automated Test Execution**: Running tests automatically
- **Test Reporting**: Generating test reports
- **Continuous Integration**: Integrating tests into development workflow

## 🔍 Common Test Scenarios

### 1. User Management Testing
```python
# Test user registration
def test_user_registration(self):
    response = self.client.post(reverse('signup'), {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'testpass123',
        'role': 'buyer'
    })
    self.assertEqual(response.status_code, 302)
    
    # Verify user was created
    user = User.objects.get(username='newuser')
    self.assertEqual(user.role, 'buyer')
```

### 2. Product Management Testing
```python
# Test product creation
def test_product_creation(self):
    self.client.login(username='seller', password='testpass123')
    response = self.client.post(reverse('product_create'), {
        'name': 'New Product',
        'description': 'New Description',
        'price': '29.99',
        'image': 'https://example.com/image.jpg'
    })
    self.assertEqual(response.status_code, 302)
    
    # Verify product was created
    product = Product.objects.get(name='New Product')
    self.assertEqual(product.price, Decimal('29.99'))
```

### 3. Shopping Cart Testing
```python
# Test add to cart
def test_add_to_cart(self):
    self.client.login(username='buyer', password='testpass123')
    response = self.client.post(
        reverse('product_detail', args=[self.product.id]),
        {'add_to_cart': 'true'}
    )
    self.assertEqual(response.status_code, 302)
    
    # Verify item was added to cart
    cart = Cart.objects.get(user=self.buyer)
    cart_item = CartItem.objects.get(cart=cart, product=self.product)
    self.assertEqual(cart_item.quantity, 1)
```

### 4. Order Processing Testing
```python
# Test checkout process
def test_checkout_process(self):
    self.client.login(username='buyer', password='testpass123')
    
    # Add item to cart
    self.client.post(
        reverse('product_detail', args=[self.product.id]),
        {'add_to_cart': 'true'}
    )
    
    # Checkout
    response = self.client.post(reverse('checkout'), {
        'address': '123 Test Street'
    })
    self.assertEqual(response.status_code, 302)
    
    # Verify order was created
    order = Order.objects.get(user=self.buyer)
    self.assertEqual(order.address, '123 Test Street')
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Issues
```bash
# Reset database
python manage.py flush
python manage.py migrate
```

#### 2. Test Data Issues
```python
# Clean up test data
from shop.test_utils import TestDataCleanup
TestDataCleanup.cleanup_test_data()
```

#### 3. Performance Test Failures
```python
# Increase performance thresholds
MAX_RESPONSE_TIME = 2.0  # Increase from 1.0 to 2.0 seconds
```

#### 4. Security Test Issues
```python
# Ensure CSRF middleware is enabled
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ... other middleware
]
```

### Debugging Tests
```python
# Enable debug output
import logging
logging.basicConfig(level=logging.DEBUG)

# Use print statements for debugging
def test_debug_example(self):
    print("Debug: Starting test")
    response = self.client.get(reverse('product_list'))
    print(f"Debug: Response status: {response.status_code}")
```

## 📚 Additional Resources

### Documentation
- [TESTING_DOCUMENTATION.md](TESTING_DOCUMENTATION.md) - Comprehensive testing documentation
- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Python Testing Documentation](https://docs.python.org/3/library/unittest.html)

### Tools and Frameworks
- [Coverage.py](https://coverage.readthedocs.io/) - Code coverage measurement
- [Pytest](https://docs.pytest.org/) - Testing framework
- [Factory Boy](https://factoryboy.readthedocs.io/) - Test data generation
- [Locust](https://locust.io/) - Load testing

### Best Practices
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [Behavior-Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development)
- [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration)

## 🤝 Contributing

To contribute to the testing laboratory:

1. **Add New Test Cases**: Create new test methods for uncovered functionality
2. **Improve Test Utilities**: Enhance the test utility classes
3. **Add New Test Categories**: Create new test categories for specific scenarios
4. **Update Documentation**: Keep documentation current with changes
5. **Report Issues**: Report bugs or issues with the testing framework

## 📄 License

This testing laboratory is part of the e-commerce application and follows the same license terms.

---

**Happy Testing! 🧪✨**

This comprehensive testing laboratory provides everything needed to learn and practice software testing methodologies in a real-world e-commerce application context. 