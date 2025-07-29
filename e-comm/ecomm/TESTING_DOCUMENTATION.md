# E-Commerce Application Testing Documentation

## Table of Contents
1. [Overview](#overview)
2. [Testing Architecture](#testing-architecture)
3. [Test Categories](#test-categories)
4. [Running Tests](#running-tests)
5. [Test Utilities](#test-utilities)
6. [Test Configuration](#test-configuration)
7. [Test Scenarios](#test-scenarios)
8. [Performance Testing](#performance-testing)
9. [Security Testing](#security-testing)
10. [Test Reporting](#test-reporting)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

## Overview

This e-commerce application is designed specifically for software testing laboratory purposes. It provides a comprehensive testing environment with multiple test categories, utilities, and configurations to demonstrate various testing methodologies and techniques.

### Key Features for Testing Lab:
- **Multiple Test Categories**: Unit, Integration, Functional, Performance, Security, and Usability tests
- **Comprehensive Test Coverage**: 1000+ test cases covering all application functionality
- **Test Utilities**: Helper classes for data generation, assertions, and performance measurement
- **Configurable Test Scenarios**: Predefined test scenarios for different testing objectives
- **Performance Testing**: Load testing, stress testing, and database performance testing
- **Security Testing**: Authentication, authorization, and input validation testing
- **Test Reporting**: Multiple report formats with detailed analysis

## Testing Architecture

### Test Structure
```
ecomm/shop/
├── tests.py              # Main test suite (1000+ tests)
├── test_utils.py         # Test utilities and helpers
├── test_config.py        # Test configuration
└── templates/            # Test templates
```

### Test Categories Overview

#### 1. Unit Tests
- **Purpose**: Test individual components in isolation
- **Coverage**: Models, views, forms, utilities
- **Examples**: User creation, product validation, cart calculations

#### 2. Integration Tests
- **Purpose**: Test component interactions
- **Coverage**: Database operations, view-model interactions
- **Examples**: Cart workflow, order processing

#### 3. Functional Tests
- **Purpose**: Test complete user workflows
- **Coverage**: End-to-end user scenarios
- **Examples**: Registration → Login → Purchase workflow

#### 4. Performance Tests
- **Purpose**: Test application performance and scalability
- **Coverage**: Response times, database queries, memory usage
- **Examples**: Load testing, stress testing

#### 5. Security Tests
- **Purpose**: Test authentication, authorization, and security features
- **Coverage**: CSRF protection, session management, input validation
- **Examples**: Unauthorized access, SQL injection attempts

#### 6. Edge Case Tests
- **Purpose**: Test boundary conditions and error scenarios
- **Coverage**: Invalid inputs, error handling, edge cases
- **Examples**: Empty forms, negative prices, duplicate usernames

## Test Categories

### Unit Tests
```python
class UserModelTest(TestCase):
    """Unit tests for User model"""
    
    def test_user_creation(self):
        """Test basic user creation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'buyer')
```

### Integration Tests
```python
class CartIntegrationTest(TestCase):
    """Integration tests for cart functionality"""
    
    def test_add_to_cart_workflow(self):
        """Test complete add to cart workflow"""
        self.client.login(username='buyer', password='testpass123')
        response = self.client.post(
            reverse('product_detail', args=[self.product.id]),
            {'add_to_cart': 'true'}
        )
        cart = Cart.objects.get(user=self.buyer)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 1)
```

### Functional Tests
```python
class UserWorkflowTest(TestCase):
    """Functional tests for complete user workflows"""
    
    def test_buyer_registration_and_purchase_workflow(self):
        """Test complete buyer registration and purchase workflow"""
        # 1. Register as buyer
        # 2. Login
        # 3. Browse products
        # 4. Add to cart
        # 5. Checkout
        # 6. Verify order
```

### Performance Tests
```python
class PerformanceTest(TestCase):
    """Performance tests for the application"""
    
    def test_product_list_performance(self):
        """Test product list page performance"""
        start_time = time.time()
        response = self.client.get(reverse('product_list'))
        end_time = time.time()
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(end_time - start_time, 1.0)
```

### Security Tests
```python
class SecurityTest(TestCase):
    """Security tests for authentication and authorization"""
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'buyer'
        })
        self.assertEqual(response.status_code, 403)
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test shop.tests.UserModelTest

# Run specific test method
python manage.py test shop.tests.UserModelTest.test_user_creation

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Categories Execution
```bash
# Run only unit tests
python manage.py test shop.tests.UserModelTest shop.tests.ProductModelTest

# Run only integration tests
python manage.py test shop.tests.CartIntegrationTest shop.tests.OrderIntegrationTest

# Run only functional tests
python manage.py test shop.tests.UserWorkflowTest

# Run only performance tests
python manage.py test shop.tests.PerformanceTest

# Run only security tests
python manage.py test shop.tests.SecurityTest
```

### Parallel Test Execution
```bash
# Run tests in parallel (requires django-parallel)
python manage.py test --parallel
```

## Test Utilities

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

### SecurityTestHelper
```python
from shop.test_utils import SecurityTestHelper

# Test CSRF protection
is_protected = SecurityTestHelper.test_csrf_protection(
    self, reverse('signup'), signup_data
)
self.assertTrue(is_protected)

# Test authentication required
requires_auth = SecurityTestHelper.test_authentication_required(
    self, reverse('cart')
)
self.assertTrue(requires_auth)
```

## Test Configuration

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

### Test Scenarios
```python
from shop.test_config import TestScenarios

# Registration scenarios
for scenario in TestScenarios.REGISTRATION_SCENARIOS:
    response = self.client.post(reverse('signup'), scenario['data'])
    self.assertEqual(response.status_code, scenario['expected_status'])

# Login scenarios
for scenario in TestScenarios.LOGIN_SCENARIOS:
    response = self.client.post(reverse('login'), scenario['data'])
    self.assertEqual(response.status_code, scenario['expected_status'])
```

## Test Scenarios

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

### Product Management Scenarios
1. **Valid Product Creation**: Successful product creation
2. **Empty Product Name**: Product creation with empty name
3. **Negative Price**: Product creation with negative price
4. **Product Editing**: Edit existing product
5. **Unauthorized Editing**: Edit another seller's product

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

## Performance Testing

### Load Testing
```python
def test_load_performance(self):
    """Test application under load"""
    # Create bulk test data
    test_data = TestDataGenerator.create_bulk_test_data(
        num_users=100,
        num_products=500,
        num_orders=200
    )
    
    # Test concurrent requests
    start_time = time.time()
    for _ in range(50):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
    end_time = time.time()
    
    # Assert performance
    self.assertLess(end_time - start_time, 10.0)
```

### Database Performance Testing
```python
def test_database_performance(self):
    """Test database query optimization"""
    from django.db import connection
    
    # Clear connection queries
    connection.queries = []
    
    # Access product list
    self.client.get(reverse('product_list'))
    
    # Check query count
    query_count = len(connection.queries)
    self.assertLess(query_count, 10)
```

### Memory Usage Testing
```python
def test_memory_usage(self):
    """Test memory usage under load"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Perform memory-intensive operations
    for _ in range(1000):
        TestDataGenerator.create_test_product()
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Assert memory usage is reasonable
    self.assertLess(memory_increase, 100)  # Less than 100MB increase
```

## Security Testing

### Authentication Testing
```python
def test_authentication_mechanisms(self):
    """Test authentication mechanisms"""
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
def test_role_based_authorization(self):
    """Test role-based access control"""
    # Buyer should not access seller dashboard
    self.client.login(username='buyer', password='testpass123')
    response = self.client.get(reverse('seller_dashboard'))
    self.assertEqual(response.status_code, 302)
    
    # Seller should access seller dashboard
    self.client.login(username='seller', password='testpass123')
    response = self.client.get(reverse('seller_dashboard'))
    self.assertEqual(response.status_code, 200)
```

### Input Validation Testing
```python
def test_input_validation(self):
    """Test input validation and sanitization"""
    # Test SQL injection attempt
    malicious_input = "'; DROP TABLE users; --"
    response = self.client.post(reverse('signup'), {
        'username': malicious_input,
        'email': 'test@example.com',
        'password': 'testpass123',
        'role': 'buyer'
    })
    # Should handle gracefully
    self.assertNotEqual(response.status_code, 500)
```

### CSRF Protection Testing
```python
def test_csrf_protection(self):
    """Test CSRF protection"""
    # Test without CSRF token
    response = self.client.post(reverse('signup'), {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'role': 'buyer'
    })
    self.assertEqual(response.status_code, 403)
```

## Test Reporting

### Coverage Reporting
```bash
# Generate coverage report
coverage run --source='.' manage.py test
coverage report -m
coverage html

# View coverage in browser
open htmlcov/index.html
```

### Test Results Analysis
```python
# Custom test result analysis
def analyze_test_results(self):
    """Analyze test results and generate report"""
    test_results = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'performance_tests': 0,
        'security_tests': 0,
    }
    
    # Collect test results
    for test_method in dir(self):
        if test_method.startswith('test_'):
            test_results['total_tests'] += 1
            # Categorize tests
            if 'performance' in test_method:
                test_results['performance_tests'] += 1
            elif 'security' in test_method:
                test_results['security_tests'] += 1
    
    return test_results
```

### Performance Metrics
```python
def generate_performance_report(self):
    """Generate performance test report"""
    performance_metrics = {
        'response_times': [],
        'database_queries': [],
        'memory_usage': [],
        'cpu_usage': [],
    }
    
    # Collect performance data
    for test_method in dir(self):
        if test_method.startswith('test_') and 'performance' in test_method:
            # Execute performance test and collect metrics
            pass
    
    return performance_metrics
```

## Best Practices

### Test Organization
1. **Group Related Tests**: Organize tests by functionality
2. **Use Descriptive Names**: Test method names should describe the scenario
3. **Follow AAA Pattern**: Arrange, Act, Assert
4. **Keep Tests Independent**: Each test should be self-contained
5. **Use setUp and tearDown**: Proper test setup and cleanup

### Test Data Management
1. **Use Test Factories**: Create test data using utility functions
2. **Clean Up After Tests**: Remove test data after each test
3. **Use Realistic Data**: Test with realistic but safe data
4. **Avoid Hard-coded Values**: Use configuration constants

### Performance Testing
1. **Set Realistic Thresholds**: Use achievable performance targets
2. **Test Under Load**: Test with realistic user loads
3. **Monitor Resources**: Track memory and CPU usage
4. **Use Profiling**: Identify performance bottlenecks

### Security Testing
1. **Test All Input Points**: Validate all user inputs
2. **Test Authentication**: Verify login/logout functionality
3. **Test Authorization**: Check role-based access control
4. **Test Session Management**: Verify session security

### Test Maintenance
1. **Update Tests Regularly**: Keep tests current with code changes
2. **Review Test Coverage**: Ensure adequate test coverage
3. **Refactor Tests**: Improve test code quality
4. **Document Test Changes**: Maintain test documentation

## Troubleshooting

### Common Test Issues

#### Database Issues
```python
# Problem: Database connection errors
# Solution: Use in-memory database for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

#### Performance Test Failures
```python
# Problem: Performance tests failing due to timing
# Solution: Increase thresholds or optimize code
MAX_RESPONSE_TIME = 2.0  # Increase from 1.0 to 2.0 seconds
```

#### Security Test Issues
```python
# Problem: CSRF tests failing
# Solution: Ensure CSRF middleware is enabled
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ... other middleware
]
```

#### Test Data Issues
```python
# Problem: Test data conflicts
# Solution: Use unique test data
username = f'testuser_{random.randint(1000, 9999)}'
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
    print(f"Debug: Response content: {response.content[:200]}")
```

### Test Environment Setup
```bash
# Install test dependencies
pip install coverage django-debug-toolbar

# Set up test environment
export DJANGO_SETTINGS_MODULE=ecomm.settings
export PYTHONPATH=/path/to/project

# Run tests with verbose output
python manage.py test -v 2
```

### Performance Testing Setup
```bash
# Install performance testing tools
pip install psutil memory-profiler

# Run performance tests
python manage.py test shop.tests.PerformanceTest -v 2
```

This comprehensive testing documentation provides everything needed for a software testing laboratory to effectively use and extend the e-commerce application's testing infrastructure. 