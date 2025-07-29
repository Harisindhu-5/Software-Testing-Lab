"""
Pytest Test Runner for E-Commerce Application
This module provides specialized test running for Pytest tests with comprehensive logging.
"""

import os
import sys
import time
import subprocess
import pytest
from pathlib import Path
from django.test import TestCase
from django.conf import settings

from .test_logger import PytestTestLogger

class PytestTestRunner:
    """Specialized test runner for Pytest tests"""
    
    def __init__(self):
        self.logger = PytestTestLogger()
        self.setup_logger()
    
    def setup_logger(self):
        """Setup logger for Pytest tests"""
        self.logger.log_test_session_start({
            'test_type': 'pytest',
            'description': 'Pytest Test Suite',
            'framework': 'pytest',
            'django_integration': True
        })
    
    def run_pytest_with_logging(self, test_path: str = "shop/tests.py", options: list = None):
        """Run Pytest with comprehensive logging"""
        if options is None:
            options = []
        
        # Build pytest command
        cmd = ["pytest", test_path, "-v"]
        cmd.extend(options)
        
        command = " ".join(cmd)
        
        self.logger.log_test_start(f"Pytest Command: {command}")
        
        start_time = time.time()
        
        try:
            # Run pytest
            result = subprocess.run(cmd, capture_output=True, text=True)
            end_time = time.time()
            duration = end_time - start_time
            
            # Log performance metric
            self.logger.log_performance_metric("Pytest Duration", duration, "seconds")
            
            # Parse pytest output
            self._parse_pytest_output(result.stdout, result.stderr)
            
            # Log result
            if result.returncode == 0:
                self.logger.log_test_success("Pytest Execution", duration, {
                    'exit_code': result.returncode,
                    'stdout_lines': len(result.stdout.split('\n')) if result.stdout else 0,
                    'stderr_lines': len(result.stderr.split('\n')) if result.stderr else 0,
                    'command': command
                })
            else:
                self.logger.log_test_failure("Pytest Execution", f"Exit code: {result.returncode}", duration, {
                    'exit_code': result.returncode,
                    'stdout_lines': len(result.stdout.split('\n')) if result.stdout else 0,
                    'stderr_lines': len(result.stderr.split('\n')) if result.stderr else 0,
                    'stderr': result.stderr,
                    'command': command
                })
            
            return result.returncode == 0
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            self.logger.log_test_failure("Pytest Execution", str(e), duration, {
                'exception_type': type(e).__name__,
                'exception_message': str(e),
                'command': command
            })
            
            return False
    
    def _parse_pytest_output(self, stdout: str, stderr: str):
        """Parse Pytest output and log individual test results"""
        if stdout:
            lines = stdout.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Parse test results
                if line.startswith('test_'):
                    if 'PASSED' in line or 'passed' in line:
                        test_name = line.split()[0]
                        self.logger.log_test_success(test_name)
                    elif 'FAILED' in line or 'failed' in line:
                        test_name = line.split()[0]
                        error_msg = line.split('FAILED')[-1] if 'FAILED' in line else line.split('failed')[-1]
                        self.logger.log_test_failure(test_name, error_msg)
                    elif 'SKIPPED' in line or 'skipped' in line:
                        test_name = line.split()[0]
                        reason = line.split('SKIPPED')[-1] if 'SKIPPED' in line else line.split('skipped')[-1]
                        self.logger.log_test_skip(test_name, reason)
                
                # Parse summary
                elif 'passed' in line and 'failed' in line:
                    self.logger.detailed_logger.info(f"Pytest Summary: {line}")
                
                # Parse warnings
                elif 'WARNING' in line or 'warning' in line:
                    self.logger.detailed_logger.warning(f"Pytest Warning: {line}")
                
                # Parse errors
                elif 'ERROR' in line or 'error' in line:
                    self.logger.detailed_logger.error(f"Pytest Error: {line}")
        
        if stderr:
            self.logger.detailed_logger.error(f"Pytest STDERR: {stderr}")
    
    def run_unit_tests_pytest(self):
        """Run unit tests using Pytest"""
        self.logger.log_test_start("Pytest Unit Tests")
        
        options = [
            "-k", "UserModelTest or ProductModelTest or CartModelTest or OrderModelTest",
            "--tb=short"
        ]
        
        return self.run_pytest_with_logging("shop/tests.py", options)
    
    def run_integration_tests_pytest(self):
        """Run integration tests using Pytest"""
        self.logger.log_test_start("Pytest Integration Tests")
        
        options = [
            "-k", "CartIntegrationTest or OrderIntegrationTest",
            "--tb=short"
        ]
        
        return self.run_pytest_with_logging("shop/tests.py", options)
    
    def run_performance_tests_pytest(self):
        """Run performance tests using Pytest"""
        self.logger.log_test_start("Pytest Performance Tests")
        
        options = [
            "-k", "PerformanceTest",
            "--tb=short"
        ]
        
        return self.run_pytest_with_logging("shop/tests.py", options)
    
    def run_security_tests_pytest(self):
        """Run security tests using Pytest"""
        self.logger.log_test_start("Pytest Security Tests")
        
        options = [
            "-k", "SecurityTest",
            "--tb=short"
        ]
        
        return self.run_pytest_with_logging("shop/tests.py", options)
    
    def run_all_tests_pytest(self):
        """Run all tests using Pytest"""
        self.logger.log_test_start("Pytest All Tests")
        
        options = [
            "--tb=short",
            "--strict-markers"
        ]
        
        return self.run_pytest_with_logging("shop/tests.py", options)
    
    def run_tests_with_coverage_pytest(self):
        """Run tests with coverage using Pytest"""
        self.logger.log_test_start("Pytest Tests with Coverage")
        
        options = [
            "--cov=shop",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--tb=short"
        ]
        
        success = self.run_pytest_with_logging("shop/tests.py", options)
        
        if success:
            self.logger.log_coverage_info({
                'coverage_type': 'pytest-cov',
                'coverage_report': 'html',
                'status': 'success'
            })
        
        return success
    
    def run_parametrized_tests(self):
        """Run parametrized tests using Pytest"""
        self.logger.log_test_start("Pytest Parametrized Tests")
        
        # Create a simple parametrized test
        test_content = '''
import pytest
from django.test import TestCase
from shop.models import User, Product

@pytest.mark.django_db
class TestParametrized:
    @pytest.mark.parametrize("username,email,role", [
        ("user1", "user1@test.com", "buyer"),
        ("user2", "user2@test.com", "seller"),
        ("user3", "user3@test.com", "buyer"),
    ])
    def test_user_creation_parametrized(self, username, email, role):
        user = User.objects.create_user(
            username=username,
            email=email,
            password="testpass123",
            role=role
        )
        assert user.username == username
        assert user.email == email
        assert user.role == role
    
    @pytest.mark.parametrize("name,price,description", [
        ("Product 1", 10.99, "Description 1"),
        ("Product 2", 20.50, "Description 2"),
        ("Product 3", 15.75, "Description 3"),
    ])
    def test_product_creation_parametrized(self, name, price, description):
        product = Product.objects.create(
            name=name,
            price=price,
            description=description
        )
        assert product.name == name
        assert product.price == price
        assert product.description == description
'''
        
        # Write temporary test file
        temp_test_file = "shop/temp_parametrized_tests.py"
        with open(temp_test_file, 'w') as f:
            f.write(test_content)
        
        try:
            options = [
                "-v",
                "--tb=short"
            ]
            
            success = self.run_pytest_with_logging(temp_test_file, options)
            
            # Log parametrized test details
            if success:
                self.logger.log_parametrized_test("test_user_creation_parametrized", {
                    'parameters': 3,
                    'test_type': 'user_creation'
                })
                self.logger.log_parametrized_test("test_product_creation_parametrized", {
                    'parameters': 3,
                    'test_type': 'product_creation'
                })
            
            return success
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_test_file):
                os.remove(temp_test_file)
    
    def run_fixture_tests(self):
        """Run tests with fixtures using Pytest"""
        self.logger.log_test_start("Pytest Fixture Tests")
        
        # Create a test with fixtures
        test_content = '''
import pytest
from django.test import TestCase
from shop.models import User, Product, Cart

@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="fixture_user",
        email="fixture@test.com",
        password="testpass123",
        role="buyer"
    )

@pytest.fixture
def test_product():
    return Product.objects.create(
        name="Fixture Product",
        price=25.99,
        description="Test product for fixtures"
    )

@pytest.fixture
def test_cart(test_user):
    return Cart.objects.create(user=test_user)

@pytest.mark.django_db
class TestWithFixtures:
    def test_user_fixture(self, test_user):
        assert test_user.username == "fixture_user"
        assert test_user.role == "buyer"
    
    def test_product_fixture(self, test_product):
        assert test_product.name == "Fixture Product"
        assert test_product.price == 25.99
    
    def test_cart_fixture(self, test_cart, test_user):
        assert test_cart.user == test_user
        assert test_cart.items.count() == 0
'''
        
        # Write temporary test file
        temp_test_file = "shop/temp_fixture_tests.py"
        with open(temp_test_file, 'w') as f:
            f.write(test_content)
        
        try:
            options = [
                "-v",
                "--tb=short"
            ]
            
            success = self.run_pytest_with_logging(temp_test_file, options)
            
            # Log fixture details
            if success:
                self.logger.log_fixture_setup("test_user")
                self.logger.log_fixture_setup("test_product")
                self.logger.log_fixture_setup("test_cart")
                self.logger.log_fixture_teardown("test_user")
                self.logger.log_fixture_teardown("test_product")
                self.logger.log_fixture_teardown("test_cart")
            
            return success
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_test_file):
                os.remove(temp_test_file)
    
    def run_all_pytest_variants(self):
        """Run all Pytest test variants"""
        test_variants = [
            ("Unit Tests", self.run_unit_tests_pytest),
            ("Integration Tests", self.run_integration_tests_pytest),
            ("Performance Tests", self.run_performance_tests_pytest),
            ("Security Tests", self.run_security_tests_pytest),
            ("Parametrized Tests", self.run_parametrized_tests),
            ("Fixture Tests", self.run_fixture_tests),
            ("Coverage Tests", self.run_tests_with_coverage_pytest),
        ]
        
        results = {}
        
        for variant_name, variant_func in test_variants:
            self.logger.log_test_start(f"Pytest {variant_name}")
            results[variant_name] = variant_func()
        
        # Log session end
        self.logger.log_test_session_end()
        
        return results

def run_pytest_tests_with_logging():
    """Run Pytest tests with comprehensive logging"""
    runner = PytestTestRunner()
    
    try:
        results = runner.run_all_pytest_variants()
        
        # Print summary to terminal
        print("\n" + "="*60)
        print("PYTEST TEST RESULTS")
        print("="*60)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<25}: {status}")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print("-" * 60)
        print(f"Total Test Variants: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "Success Rate: 0%")
        
        return all(results.values())
        
    except Exception as e:
        runner.logger.log_test_failure("Pytest Test Runner", str(e))
        runner.logger.log_test_session_end()
        return False

if __name__ == "__main__":
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
    
    # Run Pytest tests
    run_pytest_tests_with_logging() 