#!/usr/bin/env python
"""
Test Runner Script for E-Commerce Application
This script provides easy commands to run different types of tests for the software testing laboratory.
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')

# Import our test logger
from shop.test_logger import create_test_logger

def run_command_with_logging(command, description="", test_type="django"):
    """Run a command with comprehensive logging"""
    logger = create_test_logger(test_type)
    
    # Log session start
    session_info = {
        'command': command,
        'description': description,
        'test_type': test_type,
        'working_directory': os.getcwd()
    }
    logger.log_test_session_start(session_info)
    
    start_time = time.time()
    try:
        # Capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        end_time = time.time()
        duration = end_time - start_time
        
        # Log performance metric
        logger.log_performance_metric("Command Duration", duration, "seconds")
        
        # Log detailed output to file
        if result.stdout:
            logger.detailed_logger.info("STDOUT:")
            logger.detailed_logger.info(result.stdout)
        
        if result.stderr:
            logger.detailed_logger.error("STDERR:")
            logger.detailed_logger.error(result.stderr)
        
        # Log result
        if result.returncode == 0:
            logger.log_test_success(f"Command: {description}", duration, {
                'exit_code': result.returncode,
                'stdout_lines': len(result.stdout.split('\n')) if result.stdout else 0,
                'stderr_lines': len(result.stderr.split('\n')) if result.stderr else 0
            })
        else:
            logger.log_test_failure(f"Command: {description}", f"Exit code: {result.returncode}", duration, {
                'exit_code': result.returncode,
                'stdout_lines': len(result.stdout.split('\n')) if result.stdout else 0,
                'stderr_lines': len(result.stderr.split('\n')) if result.stderr else 0,
                'stderr': result.stderr
            })
        
        # Log session end
        logger.log_test_session_end()
        
        return result.returncode == 0
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        logger.log_test_failure(f"Command: {description}", str(e), duration, {
            'exception_type': type(e).__name__,
            'exception_message': str(e)
        })
        
        logger.log_test_session_end()
        return False

def run_unit_tests():
    """Run unit tests only"""
    command = "python manage.py test shop.tests.UserModelTest shop.tests.ProductModelTest shop.tests.CartModelTest shop.tests.OrderModelTest -v 2"
    return run_command_with_logging(command, "Unit Tests", "django")

def run_integration_tests():
    """Run integration tests only"""
    command = "python manage.py test shop.tests.CartIntegrationTest shop.tests.OrderIntegrationTest -v 2"
    return run_command_with_logging(command, "Integration Tests", "django")

def run_functional_tests():
    """Run functional tests only"""
    command = "python manage.py test shop.tests.UserWorkflowTest -v 2"
    return run_command_with_logging(command, "Functional Tests", "django")

def run_performance_tests():
    """Run performance tests only"""
    command = "python manage.py test shop.tests.PerformanceTest -v 2"
    return run_command_with_logging(command, "Performance Tests", "django")

def run_security_tests():
    """Run security tests only"""
    command = "python manage.py test shop.tests.SecurityTest -v 2"
    return run_command_with_logging(command, "Security Tests", "django")

def run_edge_case_tests():
    """Run edge case tests only"""
    command = "python manage.py test shop.tests.EdgeCaseTest -v 2"
    return run_command_with_logging(command, "Edge Case Tests", "django")

def run_api_tests():
    """Run API tests only"""
    command = "python manage.py test shop.tests.APITest -v 2"
    return run_command_with_logging(command, "API Tests", "django")

def run_data_validation_tests():
    """Run data validation tests only"""
    command = "python manage.py test shop.tests.DataValidationTest -v 2"
    return run_command_with_logging(command, "Data Validation Tests", "django")

def run_concurrency_tests():
    """Run concurrency tests only"""
    command = "python manage.py test shop.tests.ConcurrencyTest -v 2"
    return run_command_with_logging(command, "Concurrency Tests", "django")

def run_error_handling_tests():
    """Run error handling tests only"""
    command = "python manage.py test shop.tests.ErrorHandlingTest -v 2"
    return run_command_with_logging(command, "Error Handling Tests", "django")

def run_usability_tests():
    """Run usability tests only"""
    command = "python manage.py test shop.tests.UsabilityTest -v 2"
    return run_command_with_logging(command, "Usability Tests", "django")

def run_comprehensive_tests():
    """Run comprehensive test suite"""
    command = "python manage.py test shop.tests.ComprehensiveTestSuite -v 2"
    return run_command_with_logging(command, "Comprehensive Test Suite", "django")

def run_all_tests():
    """Run all tests"""
    command = "python manage.py test -v 2"
    return run_command_with_logging(command, "All Tests", "django")

def run_tests_with_coverage():
    """Run tests with coverage report"""
    logger = create_test_logger("coverage")
    
    logger.log_test_session_start({
        'test_type': 'coverage',
        'description': 'Tests with Coverage Report'
    })
    
    # Run tests with coverage
    coverage_command = "coverage run --source='.' manage.py test"
    success = run_command_with_logging(coverage_command, "Tests with Coverage", "coverage")
    
    if success:
        # Generate coverage report
        report_command = "coverage report -m"
        report_result = subprocess.run(report_command, shell=True, capture_output=True, text=True)
        
        if report_result.returncode == 0:
            logger.log_coverage_info({
                'coverage_report': report_result.stdout,
                'status': 'success'
            })
        else:
            logger.log_test_failure("Coverage Report Generation", report_result.stderr)
        
        # Generate HTML coverage report
        html_command = "coverage html"
        html_result = subprocess.run(html_command, shell=True, capture_output=True, text=True)
        
        if html_result.returncode == 0:
            logger.log_test_success("HTML Coverage Report Generation")
        else:
            logger.log_test_failure("HTML Coverage Report Generation", html_result.stderr)
    
    logger.log_test_session_end()
    return success

def run_performance_analysis():
    """Run performance analysis"""
    logger = create_test_logger("performance")
    
    logger.log_test_session_start({
        'test_type': 'performance',
        'description': 'Performance Analysis'
    })
    
    # Create bulk test data
    logger.log_setup_teardown("Setup", "Creating bulk test data for performance testing")
    create_data_command = "python manage.py shell -c \"from shop.test_utils import TestDataGenerator; TestDataGenerator.create_bulk_test_data(num_users=100, num_products=500, num_orders=200)\""
    run_command_with_logging(create_data_command, "Creating Test Data", "performance")
    
    # Run performance tests
    perf_command = "python manage.py test shop.tests.PerformanceTest -v 2"
    success = run_command_with_logging(perf_command, "Performance Tests", "performance")
    
    logger.log_test_session_end()
    return success

def run_security_analysis():
    """Run security analysis"""
    command = "python manage.py test shop.tests.SecurityTest -v 2"
    return run_command_with_logging(command, "Security Tests", "django")

def run_load_testing():
    """Run load testing"""
    logger = create_test_logger("load")
    
    logger.log_test_session_start({
        'test_type': 'load',
        'description': 'Load Testing'
    })
    
    # Create large dataset
    logger.log_setup_teardown("Setup", "Creating large dataset for load testing")
    load_data_command = "python manage.py shell -c \"from shop.test_utils import TestDataGenerator; TestDataGenerator.create_bulk_test_data(num_users=1000, num_products=5000, num_orders=2000)\""
    run_command_with_logging(load_data_command, "Creating Load Test Data", "load")
    
    # Run load tests
    load_command = "python manage.py test shop.tests.PerformanceTest.test_large_cart_performance shop.tests.PerformanceTest.test_product_list_performance -v 2"
    success = run_command_with_logging(load_command, "Load Tests", "load")
    
    logger.log_test_session_end()
    return success

def run_stress_testing():
    """Run stress testing"""
    logger = create_test_logger("stress")
    
    logger.log_test_session_start({
        'test_type': 'stress',
        'description': 'Stress Testing'
    })
    
    # Create stress test data
    logger.log_setup_teardown("Setup", "Creating stress test data")
    stress_data_command = "python manage.py shell -c \"from shop.test_utils import TestDataGenerator; TestDataGenerator.create_bulk_test_data(num_users=2000, num_products=10000, num_orders=5000)\""
    run_command_with_logging(stress_data_command, "Creating Stress Test Data", "stress")
    
    # Run stress tests
    stress_command = "python manage.py test shop.tests.PerformanceTest -v 2"
    success = run_command_with_logging(stress_command, "Stress Tests", "stress")
    
    logger.log_test_session_end()
    return success

def run_selenium_tests():
    """Run Selenium tests"""
    # First, make sure Django server is running
    print("[INFO] For Selenium tests, please ensure Django server is running on localhost:8000")
    print("[INFO] You can start it with: python manage.py runserver")
    
    # Run the Selenium test runner directly
    try:
        from shop.selenium_test_runner import run_selenium_tests_with_logging
        return run_selenium_tests_with_logging()
    except Exception as e:
        print(f"[ERROR] Failed to run Selenium tests: {e}")
        return False

def run_pytest_tests():
    """Run Pytest tests"""
    command = "pytest shop/tests.py -v"
    return run_command_with_logging(command, "Pytest Tests", "pytest")

def run_test_categories():
    """Run tests by categories"""
    categories = {
        'unit': run_unit_tests,
        'integration': run_integration_tests,
        'functional': run_functional_tests,
        'performance': run_performance_tests,
        'security': run_security_tests,
        'edge': run_edge_case_tests,
        'api': run_api_tests,
        'validation': run_data_validation_tests,
        'concurrency': run_concurrency_tests,
        'error': run_error_handling_tests,
        'usability': run_usability_tests,
    }
    
    print("\nAvailable test categories:")
    for category in categories.keys():
        print(f"  - {category}")
    
    category = input("\nEnter category to run (or 'all' for all categories): ").lower()
    
    if category == 'all':
        results = {}
        for name, func in categories.items():
            print(f"\nRunning {name} tests...")
            results[name] = func()
        
        print("\n" + "="*60)
        print("Test Results Summary")
        print("="*60)
        for name, success in results.items():
            status = "PASSED" if success else "FAILED"
            print(f"{name:15}: {status}")
        
        return all(results.values())
    elif category in categories:
        return categories[category]()
    else:
        print(f"Unknown category: {category}")
        return False

def run_custom_test():
    """Run a custom test"""
    print("\n" + "="*60)
    print("Custom Test Runner")
    print("="*60)
    
    print("Available test classes:")
    test_classes = [
        "UserModelTest", "ProductModelTest", "CartModelTest", "OrderModelTest",
        "CartIntegrationTest", "OrderIntegrationTest", "UserWorkflowTest",
        "PerformanceTest", "SecurityTest", "EdgeCaseTest", "APITest",
        "DataValidationTest", "ConcurrencyTest", "ErrorHandlingTest",
        "UsabilityTest", "ComprehensiveTestSuite"
    ]
    
    for i, test_class in enumerate(test_classes, 1):
        print(f"  {i:2}. {test_class}")
    
    try:
        choice = int(input("\nEnter test class number: ")) - 1
        if 0 <= choice < len(test_classes):
            test_class = test_classes[choice]
            command = f"python manage.py test shop.tests.{test_class} -v 2"
            return run_command_with_logging(command, f"Custom Test: {test_class}", "django")
        else:
            print("Invalid choice")
            return False
    except ValueError:
        print("Invalid input")
        return False

def show_test_statistics():
    """Show test statistics"""
    logger = create_test_logger("statistics")
    
    logger.log_test_session_start({
        'test_type': 'statistics',
        'description': 'Test Statistics Analysis'
    })
    
    # Count test methods in each class
    import shop.tests
    
    test_classes = [
        shop.tests.UserModelTest,
        shop.tests.ProductModelTest,
        shop.tests.CartModelTest,
        shop.tests.OrderModelTest,
        shop.tests.CartIntegrationTest,
        shop.tests.OrderIntegrationTest,
        shop.tests.UserWorkflowTest,
        shop.tests.EdgeCaseTest,
        shop.tests.PerformanceTest,
        shop.tests.SecurityTest,
        shop.tests.APITest,
        shop.tests.DataValidationTest,
        shop.tests.ConcurrencyTest,
        shop.tests.ErrorHandlingTest,
        shop.tests.UsabilityTest,
        shop.tests.ComprehensiveTestSuite,
    ]
    
    total_tests = 0
    test_stats = {}
    
    for test_class in test_classes:
        test_methods = [method for method in dir(test_class) if method.startswith('test_')]
        count = len(test_methods)
        total_tests += count
        test_stats[test_class.__name__] = count
    
    # Log statistics
    logger.log_test_success("Statistics Generation", details={
        'total_tests': total_tests,
        'test_classes': len(test_classes),
        'test_distribution': test_stats
    })
    
    # Show test categories
    categories = {
        'Unit Tests': ['UserModelTest', 'ProductModelTest', 'CartModelTest', 'OrderModelTest'],
        'Integration Tests': ['CartIntegrationTest', 'OrderIntegrationTest'],
        'Functional Tests': ['UserWorkflowTest'],
        'Performance Tests': ['PerformanceTest'],
        'Security Tests': ['SecurityTest'],
        'Edge Case Tests': ['EdgeCaseTest'],
        'API Tests': ['APITest'],
        'Data Validation Tests': ['DataValidationTest'],
        'Concurrency Tests': ['ConcurrencyTest'],
        'Error Handling Tests': ['ErrorHandlingTest'],
        'Usability Tests': ['UsabilityTest'],
        'Comprehensive Tests': ['ComprehensiveTestSuite'],
    }
    
    category_stats = {}
    for category, classes in categories.items():
        count = sum(len([m for m in dir(getattr(shop.tests, cls)) if m.startswith('test_')]) for cls in classes)
        category_stats[category] = count
    
    logger.log_test_success("Category Analysis", details={
        'category_distribution': category_stats
    })
    
    logger.log_test_session_end()
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='E-Commerce Test Runner')
    parser.add_argument('--unit', action='store_true', help='Run unit tests')
    parser.add_argument('--integration', action='store_true', help='Run integration tests')
    parser.add_argument('--functional', action='store_true', help='Run functional tests')
    parser.add_argument('--performance', action='store_true', help='Run performance tests')
    parser.add_argument('--security', action='store_true', help='Run security tests')
    parser.add_argument('--edge', action='store_true', help='Run edge case tests')
    parser.add_argument('--api', action='store_true', help='Run API tests')
    parser.add_argument('--validation', action='store_true', help='Run data validation tests')
    parser.add_argument('--concurrency', action='store_true', help='Run concurrency tests')
    parser.add_argument('--error', action='store_true', help='Run error handling tests')
    parser.add_argument('--usability', action='store_true', help='Run usability tests')
    parser.add_argument('--comprehensive', action='store_true', help='Run comprehensive tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage')
    parser.add_argument('--load', action='store_true', help='Run load testing')
    parser.add_argument('--stress', action='store_true', help='Run stress testing')
    parser.add_argument('--selenium', action='store_true', help='Run Selenium tests')
    parser.add_argument('--pytest', action='store_true', help='Run Pytest tests')
    parser.add_argument('--categories', action='store_true', help='Run tests by categories')
    parser.add_argument('--custom', action='store_true', help='Run custom test')
    parser.add_argument('--stats', action='store_true', help='Show test statistics')
    
    args = parser.parse_args()
    
    if args.unit:
        run_unit_tests()
    elif args.integration:
        run_integration_tests()
    elif args.functional:
        run_functional_tests()
    elif args.performance:
        run_performance_tests()
    elif args.security:
        run_security_tests()
    elif args.edge:
        run_edge_case_tests()
    elif args.api:
        run_api_tests()
    elif args.validation:
        run_data_validation_tests()
    elif args.concurrency:
        run_concurrency_tests()
    elif args.error:
        run_error_handling_tests()
    elif args.usability:
        run_usability_tests()
    elif args.comprehensive:
        run_comprehensive_tests()
    elif args.all:
        run_all_tests()
    elif args.coverage:
        run_tests_with_coverage()
    elif args.load:
        run_load_testing()
    elif args.stress:
        run_stress_testing()
    elif args.selenium:
        run_selenium_tests()
    elif args.pytest:
        run_pytest_tests()
    elif args.categories:
        run_test_categories()
    elif args.custom:
        run_custom_test()
    elif args.stats:
        show_test_statistics()
    else:
        # Interactive mode
        print("E-Commerce Test Runner")
        print("="*60)
        print("1. Run Unit Tests")
        print("2. Run Integration Tests")
        print("3. Run Functional Tests")
        print("4. Run Performance Tests")
        print("5. Run Security Tests")
        print("6. Run Edge Case Tests")
        print("7. Run API Tests")
        print("8. Run Data Validation Tests")
        print("9. Run Concurrency Tests")
        print("10. Run Error Handling Tests")
        print("11. Run Usability Tests")
        print("12. Run Comprehensive Tests")
        print("13. Run All Tests")
        print("14. Run Tests with Coverage")
        print("15. Run Load Testing")
        print("16. Run Stress Testing")
        print("17. Run Selenium Tests")
        print("18. Run Pytest Tests")
        print("19. Run Tests by Categories")
        print("20. Run Custom Test")
        print("21. Show Test Statistics")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            options = {
                1: run_unit_tests,
                2: run_integration_tests,
                3: run_functional_tests,
                4: run_performance_tests,
                5: run_security_tests,
                6: run_edge_case_tests,
                7: run_api_tests,
                8: run_data_validation_tests,
                9: run_concurrency_tests,
                10: run_error_handling_tests,
                11: run_usability_tests,
                12: run_comprehensive_tests,
                13: run_all_tests,
                14: run_tests_with_coverage,
                15: run_load_testing,
                16: run_stress_testing,
                17: run_selenium_tests,
                18: run_pytest_tests,
                19: run_test_categories,
                20: run_custom_test,
                21: show_test_statistics,
                0: lambda: print("Goodbye!")
            }
            
            if choice in options:
                options[choice]()
            else:
                print("Invalid choice")
                
        except ValueError:
            print("Invalid input")
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == '__main__':
    main() 