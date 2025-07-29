"""
Test configuration for the e-commerce application.
This module contains configuration settings for comprehensive testing.
"""

import os
from decimal import Decimal

# ============================================================================
# TEST ENVIRONMENT CONFIGURATION
# ============================================================================

class TestEnvironment:
    """Test environment configuration"""
    
    # Database configuration for testing
    TEST_DATABASE = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use in-memory database for faster tests
    }
    
    # Test settings
    TEST_SETTINGS = {
        'DEBUG': False,
        'SECRET_KEY': 'test-secret-key-for-testing-only',
        'ALLOWED_HOSTS': ['testserver'],
        'PASSWORD_HASHERS': [
            'django.contrib.auth.hashers.MD5PasswordHasher',  # Faster for testing
        ],
        'EMAIL_BACKEND': 'django.core.mail.backends.locmem.EmailBackend',
        'MEDIA_URL': '/test-media/',
        'STATIC_URL': '/test-static/',
    }
    
    # Performance test thresholds
    PERFORMANCE_THRESHOLDS = {
        'MAX_RESPONSE_TIME': 1.0,  # seconds
        'MAX_DATABASE_QUERIES': 10,
        'MAX_MEMORY_USAGE': 100,  # MB
        'MAX_CPU_USAGE': 80,  # percentage
    }
    
    # Security test settings
    SECURITY_SETTINGS = {
        'CSRF_ENABLED': True,
        'SESSION_COOKIE_SECURE': False,  # Allow HTTP for testing
        'CSRF_COOKIE_SECURE': False,
        'SESSION_COOKIE_HTTPONLY': True,
        'CSRF_COOKIE_HTTPONLY': True,
    }

# ============================================================================
# TEST DATA CONFIGURATION
# ============================================================================

class TestDataConfig:
    """Test data configuration"""
    
    # User test data
    USERS = {
        'buyer': {
            'username': 'testbuyer',
            'email': 'buyer@test.com',
            'password': 'testpass123',
            'role': 'buyer',
        },
        'seller': {
            'username': 'testseller',
            'email': 'seller@test.com',
            'password': 'testpass123',
            'role': 'seller',
        },
        'admin': {
            'username': 'testadmin',
            'email': 'admin@test.com',
            'password': 'testpass123',
            'role': 'buyer',  # Admin role not implemented
        }
    }
    
    # Product test data
    PRODUCTS = {
        'valid': {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': Decimal('29.99'),
            'image': 'https://via.placeholder.com/150',
        },
        'free': {
            'name': 'Free Product',
            'description': 'Free Description',
            'price': Decimal('0.00'),
            'image': 'https://via.placeholder.com/150',
        },
        'expensive': {
            'name': 'Expensive Product',
            'description': 'Expensive Description',
            'price': Decimal('999.99'),
            'image': 'https://via.placeholder.com/150',
        },
        'invalid': {
            'name': '',  # Empty name
            'description': '',  # Empty description
            'price': Decimal('-10.00'),  # Negative price
            'image': 'invalid-url',
        }
    }
    
    # Order test data
    ORDERS = {
        'valid': {
            'address': '123 Test Street, Test City, TC 12345',
            'status': 'Pending',
        },
        'invalid': {
            'address': '',  # Empty address
            'status': 'InvalidStatus',
        }
    }
    
    # Cart test data
    CART_ITEMS = {
        'single': {'quantity': 1},
        'multiple': {'quantity': 5},
        'zero': {'quantity': 0},
        'negative': {'quantity': -1},
    }

# ============================================================================
# TEST SCENARIOS CONFIGURATION
# ============================================================================

class TestScenarios:
    """Test scenarios configuration"""
    
    # User registration scenarios
    REGISTRATION_SCENARIOS = [
        {
            'name': 'valid_buyer_registration',
            'data': {
                'username': 'newbuyer',
                'email': 'newbuyer@test.com',
                'password': 'testpass123',
                'role': 'buyer'
            },
            'expected_status': 302,  # Redirect after success
        },
        {
            'name': 'valid_seller_registration',
            'data': {
                'username': 'newseller',
                'email': 'newseller@test.com',
                'password': 'testpass123',
                'role': 'seller'
            },
            'expected_status': 302,
        },
        {
            'name': 'duplicate_username',
            'data': {
                'username': 'existinguser',
                'email': 'different@test.com',
                'password': 'testpass123',
                'role': 'buyer'
            },
            'expected_status': 200,  # Stay on form
        },
        {
            'name': 'invalid_email',
            'data': {
                'username': 'testuser',
                'email': 'invalid-email',
                'password': 'testpass123',
                'role': 'buyer'
            },
            'expected_status': 200,
        },
        {
            'name': 'empty_fields',
            'data': {
                'username': '',
                'email': '',
                'password': '',
                'role': 'buyer'
            },
            'expected_status': 200,
        }
    ]
    
    # Login scenarios
    LOGIN_SCENARIOS = [
        {
            'name': 'valid_credentials',
            'data': {
                'username': 'testbuyer',
                'password': 'testpass123'
            },
            'expected_status': 302,
        },
        {
            'name': 'invalid_username',
            'data': {
                'username': 'nonexistent',
                'password': 'testpass123'
            },
            'expected_status': 200,
        },
        {
            'name': 'invalid_password',
            'data': {
                'username': 'testbuyer',
                'password': 'wrongpassword'
            },
            'expected_status': 200,
        },
        {
            'name': 'empty_credentials',
            'data': {
                'username': '',
                'password': ''
            },
            'expected_status': 200,
        }
    ]
    
    # Product creation scenarios
    PRODUCT_CREATION_SCENARIOS = [
        {
            'name': 'valid_product',
            'data': {
                'name': 'New Product',
                'description': 'New Description',
                'price': '39.99',
                'image': 'https://example.com/image.jpg'
            },
            'expected_status': 302,
        },
        {
            'name': 'empty_name',
            'data': {
                'name': '',
                'description': 'Description',
                'price': '29.99',
                'image': 'https://example.com/image.jpg'
            },
            'expected_status': 200,
        },
        {
            'name': 'negative_price',
            'data': {
                'name': 'Product',
                'description': 'Description',
                'price': '-10.00',
                'image': 'https://example.com/image.jpg'
            },
            'expected_status': 200,
        }
    ]
    
    # Checkout scenarios
    CHECKOUT_SCENARIOS = [
        {
            'name': 'valid_checkout',
            'data': {
                'address': '123 Test Street'
            },
            'expected_status': 302,
        },
        {
            'name': 'empty_address',
            'data': {
                'address': ''
            },
            'expected_status': 200,
        }
    ]

# ============================================================================
# PERFORMANCE TEST CONFIGURATION
# ============================================================================

class PerformanceTestConfig:
    """Performance test configuration"""
    
    # Load test configuration
    LOAD_TEST = {
        'num_users': 100,
        'num_products': 500,
        'num_orders': 200,
        'concurrent_requests': 10,
        'test_duration': 60,  # seconds
    }
    
    # Stress test configuration
    STRESS_TEST = {
        'max_users': 1000,
        'max_products': 10000,
        'max_orders': 5000,
        'ramp_up_time': 30,  # seconds
        'hold_time': 60,  # seconds
        'ramp_down_time': 30,  # seconds
    }
    
    # Database performance test
    DATABASE_PERFORMANCE = {
        'query_timeout': 5.0,  # seconds
        'max_queries_per_request': 10,
        'connection_pool_size': 10,
    }
    
    # Memory usage thresholds
    MEMORY_THRESHOLDS = {
        'normal_usage': 50,  # MB
        'warning_usage': 100,  # MB
        'critical_usage': 200,  # MB
    }

# ============================================================================
# SECURITY TEST CONFIGURATION
# ============================================================================

class SecurityTestConfig:
    """Security test configuration"""
    
    # Authentication test cases
    AUTHENTICATION_TESTS = [
        'test_valid_login',
        'test_invalid_credentials',
        'test_session_timeout',
        'test_logout_functionality',
        'test_password_strength',
    ]
    
    # Authorization test cases
    AUTHORIZATION_TESTS = [
        'test_role_based_access',
        'test_resource_ownership',
        'test_privilege_escalation',
        'test_unauthorized_access',
    ]
    
    # Input validation test cases
    INPUT_VALIDATION_TESTS = [
        'test_sql_injection',
        'test_xss_attack',
        'test_csrf_protection',
        'test_input_sanitization',
    ]
    
    # Session management test cases
    SESSION_TESTS = [
        'test_session_creation',
        'test_session_destruction',
        'test_session_timeout',
        'test_session_hijacking',
    ]

# ============================================================================
# TEST REPORTING CONFIGURATION
# ============================================================================

class TestReportingConfig:
    """Test reporting configuration"""
    
    # Report formats
    REPORT_FORMATS = ['html', 'xml', 'json', 'text']
    
    # Coverage thresholds
    COVERAGE_THRESHOLDS = {
        'statements': 80,
        'branches': 70,
        'functions': 80,
        'lines': 80,
    }
    
    # Test categories
    TEST_CATEGORIES = [
        'unit_tests',
        'integration_tests',
        'functional_tests',
        'performance_tests',
        'security_tests',
        'usability_tests',
    ]
    
    # Test priorities
    TEST_PRIORITIES = {
        'critical': 1,
        'high': 2,
        'medium': 3,
        'low': 4,
    }

# ============================================================================
# TEST EXECUTION CONFIGURATION
# ============================================================================

class TestExecutionConfig:
    """Test execution configuration"""
    
    # Test execution modes
    EXECUTION_MODES = {
        'unit_only': ['unit_tests'],
        'integration_only': ['integration_tests'],
        'functional_only': ['functional_tests'],
        'performance_only': ['performance_tests'],
        'security_only': ['security_tests'],
        'all_tests': ['unit_tests', 'integration_tests', 'functional_tests', 
                     'performance_tests', 'security_tests', 'usability_tests'],
    }
    
    # Test execution order
    EXECUTION_ORDER = [
        'unit_tests',
        'integration_tests',
        'functional_tests',
        'performance_tests',
        'security_tests',
        'usability_tests',
    ]
    
    # Parallel execution settings
    PARALLEL_EXECUTION = {
        'enabled': True,
        'max_workers': 4,
        'timeout': 300,  # seconds
    }
    
    # Test retry settings
    RETRY_SETTINGS = {
        'max_retries': 3,
        'retry_delay': 1,  # seconds
        'retry_on_failure': True,
    }

# ============================================================================
# ENVIRONMENT-SPECIFIC CONFIGURATIONS
# ============================================================================

class EnvironmentConfig:
    """Environment-specific configurations"""
    
    # Development environment
    DEVELOPMENT = {
        'debug': True,
        'database': 'sqlite3',
        'cache': 'locmem',
        'email': 'console',
        'logging': 'debug',
    }
    
    # Testing environment
    TESTING = {
        'debug': False,
        'database': 'sqlite3',
        'cache': 'locmem',
        'email': 'locmem',
        'logging': 'warning',
    }
    
    # Staging environment
    STAGING = {
        'debug': False,
        'database': 'postgresql',
        'cache': 'redis',
        'email': 'smtp',
        'logging': 'info',
    }
    
    # Production environment
    PRODUCTION = {
        'debug': False,
        'database': 'postgresql',
        'cache': 'redis',
        'email': 'smtp',
        'logging': 'error',
    } 