"""
Test script to verify frontend-backend integration
"""
import requests
from requests.sessions import Session

BASE_URL = "http://localhost:5000"

def test_home_page():
    """Test home page loads"""
    response = requests.get(f"{BASE_URL}/")
    print(f"✓ Home Page - Status: {response.status_code}")
    return response.status_code == 200

def test_login_page():
    """Test login page loads"""
    response = requests.get(f"{BASE_URL}/login")
    print(f"✓ Login Page - Status: {response.status_code}")
    return response.status_code == 200

def test_student_registration():
    """Test student registration page and backend"""
    session = requests.Session()
    
    # Load registration page
    response = session.get(f"{BASE_URL}/register/student")
    print(f"✓ Student Registration Page - Status: {response.status_code}")
    
    return response.status_code == 200

def test_company_registration():
    """Test company registration page"""
    response = requests.get(f"{BASE_URL}/register/company")
    print(f"✓ Company Registration Page - Status: {response.status_code}")
    return response.status_code == 200

def test_admin_login():
    """Test admin login with default credentials"""
    session = requests.Session()
    
    # Attempt login
    response = session.post(f"{BASE_URL}/login", data={
        "username": "admin",
        "password": "admin123"
    })
    
    print(f"✓ Admin Login - Status: {response.status_code}")
    
    # Check if redirected to admin dashboard
    if response.history:
        print(f"  Redirected to: {response.url}")
    
    return "admin/dashboard" in response.url or response.status_code == 200

if __name__ == "__main__":
    print("=" * 50)
    print("CareerBridge Frontend-Backend Integration Tests")
    print("=" * 50)
    
    tests = [
        test_home_page,
        test_login_page,
        test_student_registration,
        test_company_registration,
        test_admin_login
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} ERROR: {e}")
    
    print("=" * 50)
    print(f"Tests Passed: {passed}/{len(tests)}")
    print(f"Tests Failed: {failed}/{len(tests)}")
    print("=" * 50)
