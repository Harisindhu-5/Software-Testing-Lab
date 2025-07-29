"""
Test Logger for E-Commerce Application
This module provides comprehensive logging for different test types.
"""

import logging
import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class TestLogger:
    """Comprehensive test logger for different test types"""
    
    def __init__(self, test_type: str, log_dir: str = "test_logs"):
        """
        Initialize test logger
        
        Args:
            test_type: Type of test (selenium, pytest, django, etc.)
            log_dir: Directory to store log files
        """
        self.test_type = test_type
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamp for this test run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize loggers
        self._setup_loggers()
        
        # Test statistics
        self.test_stats = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'skipped_tests': 0,
            'start_time': time.time(),
            'end_time': None,
            'duration': None,
            'test_details': []
        }
    
    def _setup_loggers(self):
        """Setup different loggers for different purposes"""
        
        # Main detailed logger (writes to file)
        self.detailed_logger = logging.getLogger(f"{self.test_type}_detailed")
        self.detailed_logger.setLevel(logging.DEBUG)
        
        # Create detailed log file
        detailed_log_file = self.log_dir / f"{self.test_type}_detailed_{self.timestamp}.log"
        detailed_handler = logging.FileHandler(detailed_log_file, encoding='utf-8')
        detailed_handler.setLevel(logging.DEBUG)
        
        # Create detailed formatter
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        detailed_handler.setFormatter(detailed_formatter)
        
        self.detailed_logger.addHandler(detailed_handler)
        self.detailed_logger.propagate = False
        
        # Summary logger (writes to file)
        self.summary_logger = logging.getLogger(f"{self.test_type}_summary")
        self.summary_logger.setLevel(logging.INFO)
        
        # Create summary log file
        summary_log_file = self.log_dir / f"{self.test_type}_summary_{self.timestamp}.log"
        summary_handler = logging.FileHandler(summary_log_file, encoding='utf-8')
        summary_handler.setLevel(logging.INFO)
        
        # Create summary formatter
        summary_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        summary_handler.setFormatter(summary_formatter)
        
        self.summary_logger.addHandler(summary_handler)
        self.summary_logger.propagate = False
        
        # Error logger (writes to file)
        self.error_logger = logging.getLogger(f"{self.test_type}_errors")
        self.error_logger.setLevel(logging.ERROR)
        
        # Create error log file
        error_log_file = self.log_dir / f"{self.test_type}_errors_{self.timestamp}.log"
        error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
        error_handler.setLevel(logging.ERROR)
        
        # Create error formatter
        error_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s\n'
        )
        error_handler.setFormatter(error_formatter)
        
        self.error_logger.addHandler(error_handler)
        self.error_logger.propagate = False
        
        # Performance logger (writes to file)
        self.performance_logger = logging.getLogger(f"{self.test_type}_performance")
        self.performance_logger.setLevel(logging.INFO)
        
        # Create performance log file
        performance_log_file = self.log_dir / f"{self.test_type}_performance_{self.timestamp}.log"
        performance_handler = logging.FileHandler(performance_log_file, encoding='utf-8')
        performance_handler.setLevel(logging.INFO)
        
        # Create performance formatter
        performance_formatter = logging.Formatter(
            '%(asctime)s - %(message)s'
        )
        performance_handler.setFormatter(performance_formatter)
        
        self.performance_logger.addHandler(performance_handler)
        self.performance_logger.propagate = False
    
    def log_test_start(self, test_name: str, test_class: str = None):
        """Log test start"""
        message = f"Starting test: {test_name}"
        if test_class:
            message += f" in class: {test_class}"
        
        self.detailed_logger.info(message)
        self.test_stats['total_tests'] += 1
        
        # Terminal output (without emoji for Windows compatibility)
        print(f"[RUNNING] {test_name}")
    
    def log_test_success(self, test_name: str, duration: float = None, details: Dict = None):
        """Log successful test"""
        message = f"[PASS] Test PASSED: {test_name}"
        if duration:
            message += f" (Duration: {duration:.2f}s)"
        
        self.detailed_logger.info(message)
        self.summary_logger.info(f"PASS: {test_name}")
        
        if details:
            self.detailed_logger.debug(f"Test details: {json.dumps(details, indent=2)}")
        
        self.test_stats['passed_tests'] += 1
        self.test_stats['test_details'].append({
            'name': test_name,
            'status': 'PASS',
            'duration': duration,
            'details': details
        })
        
        # Terminal output (without emoji for Windows compatibility)
        print(f"[PASS] {test_name}")
    
    def log_test_failure(self, test_name: str, error: str, duration: float = None, details: Dict = None):
        """Log failed test"""
        message = f"[FAIL] Test FAILED: {test_name}"
        if duration:
            message += f" (Duration: {duration:.2f}s)"
        
        self.detailed_logger.error(message)
        self.detailed_logger.error(f"Error: {error}")
        self.summary_logger.error(f"FAIL: {test_name} - {error}")
        self.error_logger.error(f"FAIL: {test_name}\nError: {error}")
        
        if details:
            self.detailed_logger.debug(f"Test details: {json.dumps(details, indent=2)}")
        
        self.test_stats['failed_tests'] += 1
        self.test_stats['test_details'].append({
            'name': test_name,
            'status': 'FAIL',
            'duration': duration,
            'error': error,
            'details': details
        })
        
        # Terminal output (without emoji for Windows compatibility)
        print(f"[FAIL] {test_name}")
    
    def log_test_skip(self, test_name: str, reason: str = None):
        """Log skipped test"""
        message = f"[SKIP] Test SKIPPED: {test_name}"
        if reason:
            message += f" (Reason: {reason})"
        
        self.detailed_logger.warning(message)
        self.summary_logger.warning(f"SKIP: {test_name}")
        
        self.test_stats['skipped_tests'] += 1
        self.test_stats['test_details'].append({
            'name': test_name,
            'status': 'SKIP',
            'reason': reason
        })
        
        # Terminal output (without emoji for Windows compatibility)
        print(f"[SKIP] {test_name}")
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = None):
        """Log performance metrics"""
        message = f"{metric_name}: {value}"
        if unit:
            message += f" {unit}"
        
        self.performance_logger.info(message)
        self.detailed_logger.info(f"Performance - {message}")
    
    def log_database_operation(self, operation: str, details: Dict = None):
        """Log database operations"""
        message = f"Database operation: {operation}"
        self.detailed_logger.info(message)
        
        if details:
            self.detailed_logger.debug(f"Database details: {json.dumps(details, indent=2)}")
        
        # Terminal output (without emoji for Windows compatibility)
        print(f"[DB] {operation}")
    
    def log_selenium_action(self, action: str, element: str = None, value: str = None):
        """Log Selenium actions"""
        message = f"Selenium action: {action}"
        if element:
            message += f" on element: {element}"
        if value:
            message += f" with value: {value}"
        
        self.detailed_logger.info(message)
    
    def log_setup_teardown(self, phase: str, details: str = None):
        """Log setup/teardown operations"""
        message = f"{phase.upper()}: {details}" if details else f"{phase.upper()}"
        self.detailed_logger.info(message)
        
        # Terminal output for important setup/teardown (without emoji for Windows compatibility)
        if phase.lower() in ['setup', 'teardown']:
            print(f"[SETUP] {phase.upper()}: {details}")
    
    def log_coverage_info(self, coverage_data: Dict):
        """Log coverage information"""
        self.detailed_logger.info("Coverage Report:")
        self.detailed_logger.info(json.dumps(coverage_data, indent=2))
        
        # Terminal output (without emoji for Windows compatibility)
        if 'total' in coverage_data:
            print(f"[COVERAGE] {coverage_data['total']}%")
    
    def log_test_session_start(self, session_info: Dict):
        """Log test session start"""
        self.detailed_logger.info("=" * 60)
        self.detailed_logger.info("TEST SESSION STARTED")
        self.detailed_logger.info("=" * 60)
        self.detailed_logger.info(f"Test Type: {self.test_type}")
        self.detailed_logger.info(f"Timestamp: {self.timestamp}")
        self.detailed_logger.info(f"Session Info: {json.dumps(session_info, indent=2)}")
        
        # Terminal output (without emoji for Windows compatibility)
        print(f"[START] Starting {self.test_type.upper()} tests...")
        print(f"[LOGS] Logs: {self.log_dir}")
    
    def log_test_session_end(self):
        """Log test session end and generate summary"""
        self.test_stats['end_time'] = time.time()
        self.test_stats['duration'] = self.test_stats['end_time'] - self.test_stats['start_time']
        
        # Generate summary
        summary = self._generate_summary()
        
        # Log summary
        self.detailed_logger.info("=" * 60)
        self.detailed_logger.info("TEST SESSION ENDED")
        self.detailed_logger.info("=" * 60)
        self.detailed_logger.info(summary)
        
        self.summary_logger.info("=" * 60)
        self.summary_logger.info("TEST SUMMARY")
        self.summary_logger.info("=" * 60)
        self.summary_logger.info(summary)
        
        # Save detailed statistics to JSON file
        stats_file = self.log_dir / f"{self.test_type}_stats_{self.timestamp}.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_stats, f, indent=2, default=str)
        
        # Terminal output (without emoji for Windows compatibility)
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.test_stats['total_tests']}")
        print(f"Passed: {self.test_stats['passed_tests']}")
        print(f"Failed: {self.test_stats['failed_tests']}")
        print(f"Skipped: {self.test_stats['skipped_tests']}")
        print(f"Duration: {self.test_stats['duration']:.2f}s")
        
        # Fix division by zero error
        if self.test_stats['total_tests'] > 0:
            success_rate = (self.test_stats['passed_tests']/self.test_stats['total_tests']*100)
            print(f"Success Rate: {success_rate:.1f}%")
        else:
            print("Success Rate: 0%")
        
        print(f"Logs saved to: {self.log_dir}")
    
    def _generate_summary(self) -> str:
        """Generate test summary"""
        total = self.test_stats['total_tests']
        passed = self.test_stats['passed_tests']
        failed = self.test_stats['failed_tests']
        skipped = self.test_stats['skipped_tests']
        duration = self.test_stats['duration']
        
        # Fix division by zero error
        if total > 0:
            success_rate = (passed / total * 100)
            avg_duration = duration / total
        else:
            success_rate = 0
            avg_duration = 0
        
        summary = f"""
Test Session Summary:
====================
Test Type: {self.test_type}
Timestamp: {self.timestamp}
Duration: {duration:.2f} seconds

Test Results:
-------------
Total Tests: {total}
Passed: {passed}
Failed: {failed}
Skipped: {skipped}
Success Rate: {success_rate:.1f}%

Performance Metrics:
-------------------
Average Test Duration: {avg_duration:.2f}s (if applicable)

Log Files:
----------
Detailed Log: {self.test_type}_detailed_{self.timestamp}.log
Summary Log: {self.test_type}_summary_{self.timestamp}.log
Error Log: {self.test_type}_errors_{self.timestamp}.log
Performance Log: {self.test_type}_performance_{self.timestamp}.log
Statistics: {self.test_type}_stats_{self.timestamp}.json
"""
        return summary
    
    def get_log_files(self) -> Dict[str, str]:
        """Get list of log files created"""
        return {
            'detailed': f"{self.test_type}_detailed_{self.timestamp}.log",
            'summary': f"{self.test_type}_summary_{self.timestamp}.log",
            'errors': f"{self.test_type}_errors_{self.timestamp}.log",
            'performance': f"{self.test_type}_performance_{self.timestamp}.log",
            'stats': f"{self.test_type}_stats_{self.timestamp}.json"
        }

class SeleniumTestLogger(TestLogger):
    """Specialized logger for Selenium tests"""
    
    def __init__(self):
        super().__init__("selenium")
    
    def log_browser_action(self, action: str, url: str = None, element: str = None):
        """Log browser-specific actions"""
        message = f"Browser action: {action}"
        if url:
            message += f" on URL: {url}"
        if element:
            message += f" targeting element: {element}"
        
        self.detailed_logger.info(message)
    
    def log_screenshot(self, screenshot_path: str, description: str = None):
        """Log screenshot taken"""
        message = f"Screenshot saved: {screenshot_path}"
        if description:
            message += f" - {description}"
        
        self.detailed_logger.info(message)
    
    def log_page_load(self, url: str, load_time: float):
        """Log page load performance"""
        self.log_performance_metric("Page Load Time", load_time, "seconds")
        self.detailed_logger.info(f"Page loaded: {url} in {load_time:.2f}s")

class PytestTestLogger(TestLogger):
    """Specialized logger for Pytest tests"""
    
    def __init__(self):
        super().__init__("pytest")
    
    def log_fixture_setup(self, fixture_name: str):
        """Log fixture setup"""
        self.log_setup_teardown("Fixture Setup", fixture_name)
    
    def log_fixture_teardown(self, fixture_name: str):
        """Log fixture teardown"""
        self.log_setup_teardown("Fixture Teardown", fixture_name)
    
    def log_parametrized_test(self, test_name: str, params: Dict):
        """Log parametrized test execution"""
        self.detailed_logger.info(f"Parametrized test: {test_name} with params: {json.dumps(params)}")

class DjangoTestLogger(TestLogger):
    """Specialized logger for Django tests"""
    
    def __init__(self):
        super().__init__("django")
    
    def log_database_transaction(self, operation: str, model: str = None):
        """Log database transactions"""
        message = f"Database transaction: {operation}"
        if model:
            message += f" on model: {model}"
        
        self.detailed_logger.info(message)
    
    def log_migration(self, migration_name: str):
        """Log database migrations"""
        self.log_database_operation(f"Migration: {migration_name}")
    
    def log_static_files(self, static_file: str):
        """Log static file operations"""
        self.detailed_logger.info(f"Static file accessed: {static_file}")

class CoverageTestLogger(TestLogger):
    """Specialized logger for coverage tests"""
    
    def __init__(self):
        super().__init__("coverage")
    
    def log_coverage_line(self, file_path: str, line_number: int, covered: bool):
        """Log individual line coverage"""
        status = "COVERED" if covered else "MISSED"
        self.detailed_logger.debug(f"Line {line_number} in {file_path}: {status}")
    
    def log_file_coverage(self, file_path: str, coverage_percentage: float):
        """Log file coverage percentage"""
        self.log_performance_metric(f"File Coverage: {file_path}", coverage_percentage, "%")
    
    def log_branch_coverage(self, file_path: str, branch_coverage: float):
        """Log branch coverage"""
        self.log_performance_metric(f"Branch Coverage: {file_path}", branch_coverage, "%")

# Factory function to create appropriate logger
def create_test_logger(test_type: str) -> TestLogger:
    """Create appropriate test logger based on test type"""
    logger_map = {
        'selenium': SeleniumTestLogger,
        'pytest': PytestTestLogger,
        'django': DjangoTestLogger,
        'coverage': CoverageTestLogger
    }
    
    logger_class = logger_map.get(test_type.lower(), TestLogger)
    return logger_class() if test_type.lower() in logger_map else TestLogger(test_type) 