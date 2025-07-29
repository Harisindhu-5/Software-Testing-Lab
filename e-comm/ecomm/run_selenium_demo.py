#!/usr/bin/env python
"""
Selenium Test Demo Script
This script demonstrates running Selenium tests with comprehensive logging.
"""

import os
import sys
import subprocess
import time

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')

def run_selenium_tests():
    """Run Selenium tests with logging"""
    print("🚀 Starting Selenium Tests with Logging...")
    print("="*60)
    
    # Run the Selenium test runner
    try:
        result = subprocess.run([
            sys.executable, "shop/selenium_test_runner.py"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        print("Selenium Test Runner Output:")
        print("-" * 40)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Selenium tests completed successfully!")
        else:
            print("❌ Selenium tests failed!")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running Selenium tests: {e}")
        return False

def run_django_selenium_tests():
    """Run Django Selenium tests"""
    print("🚀 Starting Django Selenium Tests...")
    print("="*60)
    
    try:
        result = subprocess.run([
            sys.executable, "manage.py", "test", "shop.selenium_tests.SeleniumWebDriverTest", "-v", "2"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        print("Django Selenium Test Output:")
        print("-" * 40)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Django Selenium tests completed successfully!")
        else:
            print("❌ Django Selenium tests failed!")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running Django Selenium tests: {e}")
        return False

def show_log_files():
    """Show available log files"""
    print("\n📁 Available Log Files:")
    print("="*60)
    
    log_dir = "test_logs"
    if os.path.exists(log_dir):
        files = os.listdir(log_dir)
        if files:
            for file in sorted(files):
                file_path = os.path.join(log_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"📄 {file} ({file_size} bytes)")
        else:
            print("No log files found.")
    else:
        print("Log directory not found.")

def main():
    """Main function"""
    print("Selenium Test Demo")
    print("="*60)
    print("1. Run Selenium Test Runner")
    print("2. Run Django Selenium Tests")
    print("3. Show Log Files")
    print("4. Run Both")
    print("0. Exit")
    
    try:
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            run_selenium_tests()
        elif choice == "2":
            run_django_selenium_tests()
        elif choice == "3":
            show_log_files()
        elif choice == "4":
            print("\nRunning both test types...")
            run_selenium_tests()
            print("\n" + "="*60)
            run_django_selenium_tests()
        elif choice == "0":
            print("Goodbye!")
        else:
            print("Invalid choice!")
            
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 