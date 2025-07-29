# Quick Start Guide - Test Logging System

## 🚀 **Fixed Issues**

✅ **Unicode encoding errors** - Removed emoji characters for Windows compatibility  
✅ **Division by zero errors** - Added proper error handling  
✅ **Selenium test failures** - Fixed element selectors and assertions  
✅ **Log file encoding** - Added UTF-8 encoding for all log files  

## 🧪 **How to Run Tests**

### **1. Basic Setup**
```bash
cd ecomm
pip install -r requirements-testing.txt
python manage.py migrate
```

### **2. Run Different Test Types**

#### **Django Tests (Recommended)**
```bash
# Run all Django tests
python run_tests.py --all

# Run specific test categories
python run_tests.py --unit
python run_tests.py --integration
python run_tests.py --performance
python run_tests.py --security
```

#### **Selenium Tests**
```bash
# Option 1: Start Django server first, then run tests
python manage.py runserver &
python run_tests.py --selenium

# Option 2: Use the automated script
python run_selenium_with_server.py

# Option 3: Run directly
python shop/selenium_test_runner.py
```

#### **Pytest Tests**
```bash
python run_tests.py --pytest
```

#### **Tests with Coverage**
```bash
python run_tests.py --coverage
```

### **3. Interactive Mode**
```bash
python run_tests.py
# Then select from the menu
```

## 📁 **Log Files Created**

When you run tests, you'll get these log files in the `test_logs` directory:

- `django_detailed_*.log` - Complete test execution details
- `django_summary_*.log` - High-level test results
- `django_errors_*.log` - Error tracking and debugging
- `django_performance_*.log` - Performance metrics
- `django_stats_*.json` - Structured test data

## 🖥️ **Terminal Output (Fixed)**

**Before (with errors):**
```
🚀 Starting SELENIUM tests...
❌ FAIL: Command: Selenium Tests
UnicodeEncodeError: 'charmap' codec can't encode character '\u274c'
```

**After (fixed):**
```
[START] Starting SELENIUM tests...
[LOGS] Logs: test_logs
[RUNNING] User Registration Test
[PASS] User Registration Test
[RUNNING] User Login Test
[PASS] User Login Test
[RUNNING] Product Browsing Test
[PASS] Product Browsing Test

============================================================
TEST SUMMARY
============================================================
Total Tests: 7
Passed: 7
Failed: 0
Duration: 12.34s
Success Rate: 100.0%
Logs saved to: test_logs
```

## 🔧 **Troubleshooting**

### **Selenium Tests Not Working**
1. Make sure Django server is running: `python manage.py runserver`
2. Check if Chrome is installed
3. Try the automated script: `python run_selenium_with_server.py`

### **Log Files Not Created**
1. Check if `test_logs` directory exists
2. Ensure you have write permissions
3. Check if any antivirus is blocking file creation

### **Encoding Issues**
1. The system now uses UTF-8 encoding for all log files
2. Terminal output uses ASCII-safe characters
3. No more Unicode encoding errors on Windows

## 📊 **What You Get**

✅ **Clean terminal output** - No more encoding errors  
✅ **Detailed log files** - Complete test execution details  
✅ **Performance metrics** - Execution times and memory usage  
✅ **Error tracking** - Stack traces and debugging info  
✅ **JSON statistics** - Structured data for analysis  
✅ **Multiple test frameworks** - Django, Selenium, Pytest support  

## 🎯 **Quick Commands**

```bash
# Run all tests with logging
python run_tests.py --all

# Run Selenium tests (with server)
python run_selenium_with_server.py

# Run with coverage
python run_tests.py --coverage

# Show test statistics
python run_tests.py --stats
```

The test logging system is now fully functional and ready for your software testing laboratory! 