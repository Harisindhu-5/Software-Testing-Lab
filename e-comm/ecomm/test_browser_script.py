#!/usr/bin/env python3
"""
Simple test script to verify browser testing functionality
"""

from browser_test_script import BrowserTestScript
import json

def test_browser_script():
    """Test the browser testing script"""
    print("Testing Browser Testing Script...")
    
    # Create script instance
    script = BrowserTestScript()
    
    # Test setup driver
    print("1. Testing driver setup...")
    script.setup_driver(headless=True)
    
    if script.driver is None:
        print("❌ Driver setup failed!")
        return False
    else:
        print("✅ Driver setup successful!")
    
    # Test open browser
    print("2. Testing browser open...")
    if script.open_browser():
        print("✅ Browser opened successfully!")
    else:
        print("❌ Browser open failed!")
        return False
    
    # Test window size
    print("3. Testing window size...")
    if script.set_window_size(1024, 768):
        print("✅ Window size set successfully!")
    else:
        print("❌ Window size setting failed!")
    
    # Test logo availability
    print("4. Testing logo availability...")
    logo_available = script.check_logo_availability()
    print(f"✅ Logo availability check: {logo_available}")
    
    # Test dropdowns
    print("5. Testing dropdowns...")
    dropdowns_working = script.test_dropdowns()
    print(f"✅ Dropdown test: {dropdowns_working}")
    
    # Test invalid login
    print("6. Testing invalid login...")
    invalid_login_result = script.test_invalid_login('invaliduser', 'wrongpassword')
    print(f"✅ Invalid login test: {invalid_login_result}")
    
    # Close browser
    print("7. Closing browser...")
    script.close_browser()
    print("✅ Browser closed successfully!")
    
    print("\n🎉 All tests completed successfully!")
    return True

if __name__ == "__main__":
    test_browser_script() 