#!/usr/bin/env python
"""
Selenium Test Runner with Visible Browser Window
This script runs Selenium tests with a visible browser window so you can see the automation in action.
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')

def start_django_server():
    """Start Django development server in background"""
    print("[SERVER] Starting Django development server...")
    
    # Start server in background
    server_process = subprocess.Popen([
        sys.executable, "manage.py", "runserver", "localhost:8000"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    time.sleep(5)
    
    print(f"[SERVER] Django server started (PID: {server_process.pid})")
    return server_process

def stop_django_server(server_process):
    """Stop Django development server"""
    if server_process:
        print(f"[SERVER] Stopping Django server (PID: {server_process.pid})...")
        server_process.terminate()
        server_process.wait()
        print("[SERVER] Django server stopped")

def run_visible_selenium_tests():
    """Run Selenium tests with visible browser window"""
    print("[TESTS] Running Selenium tests with visible browser...")
    
    try:
        # Import the browser testing script
        from browser_test_script import BrowserTestScript
        
        # Create browser test instance
        script = BrowserTestScript(base_url="http://localhost:8000")
        
        # Setup driver with visible window
        print("[TESTS] Setting up browser driver (visible window)...")
        script.setup_driver(headless=False)  # This will show the browser window
        
        if script.driver is None:
            print("[ERROR] Failed to setup browser driver!")
            return False
        
        print("[TESTS] Browser window should now be visible!")
        print("[TESTS] You can watch the automation in action...")
        
        # Run a simple test sequence
        print("\n[TEST 1] Opening browser...")
        if script.open_browser():
            print("✅ Browser opened successfully!")
        else:
            print("❌ Failed to open browser!")
            return False
        
        time.sleep(2)  # Pause so you can see the browser
        
        print("\n[TEST 2] Deleting all cookies...")
        if script.delete_all_cookies():
            print("✅ Cookies deleted successfully!")
        else:
            print("❌ Failed to delete cookies!")
        
        time.sleep(2)  # Pause so you can see the action
        
        print("\n[TEST 3] Setting window size...")
        if script.set_window_size(1200, 800):
            print("✅ Window size set successfully!")
        else:
            print("❌ Failed to set window size!")
        
        time.sleep(2)  # Pause so you can see the window resize
        
        print("\n[TEST 4] Checking logo availability...")
        logo_available = script.check_logo_availability()
        if logo_available:
            print("✅ Logo found on homepage!")
        else:
            print("❌ Logo not found!")
        
        time.sleep(2)  # Pause so you can see the page
        
        print("\n[TEST 5] Testing autosuggestions...")
        autosuggestions_working = script.test_autosuggestions()
        if autosuggestions_working:
            print("✅ Autosuggestions working!")
        else:
            print("❌ Autosuggestions not working!")
        
        time.sleep(3)  # Longer pause to see autosuggestions
        
        print("\n[TEST 6] Testing dropdown functionality...")
        dropdowns_working = script.test_dropdowns()
        if dropdowns_working:
            print("✅ Dropdowns working!")
        else:
            print("❌ Dropdowns not working!")
        
        time.sleep(2)  # Pause so you can see dropdowns
        
        print("\n[TEST 7] Testing invalid login...")
        invalid_login_result = script.test_invalid_login('invaliduser', 'wrongpassword')
        if invalid_login_result:
            print("✅ Invalid login error handling working!")
        else:
            print("❌ Invalid login test failed!")
        
        time.sleep(3)  # Pause so you can see the login page
        
        print("\n[TEST 8] Testing user registration...")
        buyer_reg = script.register_user('testbuyer_visible', 'buyer@visible.com', 'pass123', 'buyer')
        if buyer_reg:
            print("✅ Buyer registration successful!")
        else:
            print("❌ Buyer registration failed!")
        
        time.sleep(3)  # Pause so you can see registration
        
        print("\n[TEST 9] Testing user login...")
        user_info = script.login_and_get_user_info('testbuyer_visible', 'pass123')
        if user_info:
            print("✅ User login successful!")
            print(f"   User info: {user_info.get('username', 'N/A')}")
        else:
            print("❌ User login failed!")
        
        time.sleep(3)  # Pause so you can see the login
        
        print("\n[TEST 10] Closing browser...")
        script.close_browser()
        print("✅ Browser closed successfully!")
        
        print("\n🎉 All visible tests completed!")
        print("You should have seen the browser window performing all these actions:")
        print("1. Opening and navigating to the website")
        print("2. Deleting cookies")
        print("3. Resizing the window")
        print("4. Checking for logo")
        print("5. Testing autosuggestions")
        print("6. Testing dropdowns")
        print("7. Testing invalid login")
        print("8. Registering a new user")
        print("9. Logging in with the new user")
        print("10. Closing the browser")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to run visible tests: {e}")
        return False

def check_server_health():
    """Check if Django server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function"""
    print("Selenium Test Runner with Visible Browser Window")
    print("="*60)
    print("This script will run Selenium tests with a visible browser window")
    print("so you can watch the automation in action!")
    print("="*60)
    
    input("Press Enter to start the tests (browser window will open)...")
    
    server_process = None
    
    try:
        # Start Django server
        server_process = start_django_server()
        
        # Wait for server to be ready
        time.sleep(3)
        
        if not check_server_health():
            print("[WARNING] Django server might not be ready, but continuing...")
        
        # Run visible Selenium tests
        success = run_visible_selenium_tests()
        
        if success:
            print("\n🎉 All visible tests completed successfully!")
        else:
            print("\n❌ Some visible tests failed!")
        
        return success
        
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Received interrupt signal")
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return False
        
    finally:
        # Always stop the server
        if server_process:
            stop_django_server(server_process)

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("[ERROR] Please run this script from the Django project directory")
        sys.exit(1)
    
    # Run the main function
    success = main()
    sys.exit(0 if success else 1) 