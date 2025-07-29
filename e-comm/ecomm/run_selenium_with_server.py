#!/usr/bin/env python
"""
Selenium Test Runner with Django Server
This script starts the Django development server and runs Selenium tests.
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

def run_selenium_tests():
    """Run Selenium tests"""
    print("[TESTS] Running Selenium tests...")
    
    try:
        # Import and run the Selenium test runner
        from shop.selenium_test_runner import run_selenium_tests_with_logging
        return run_selenium_tests_with_logging()
    except Exception as e:
        print(f"[ERROR] Failed to run Selenium tests: {e}")
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
    print("Selenium Test Runner with Django Server")
    print("="*60)
    
    server_process = None
    
    try:
        # Start Django server
        server_process = start_django_server()
        
        # Wait a bit more for server to be ready
        time.sleep(3)
        
        # Check if server is running
        if not check_server_health():
            print("[WARNING] Django server might not be ready, but continuing...")
        
        # Run Selenium tests
        success = run_selenium_tests()
        
        if success:
            print("\n[SUCCESS] All Selenium tests passed!")
        else:
            print("\n[FAILURE] Some Selenium tests failed!")
        
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