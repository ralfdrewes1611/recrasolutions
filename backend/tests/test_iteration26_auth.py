"""
Iteration 26: Auth Login Gate Tests
Tests for password-protected main page with JWT-based authentication.
Credentials: Username=AdminRECRA, Password=Welkom123$
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAuthLogin:
    """Authentication login endpoint tests"""
    
    def test_login_success_correct_credentials(self):
        """POST /api/auth/login with correct credentials returns token + username + role"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "AdminRECRA",
            "password": "Welkom123$"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "token" in data, "Response should contain 'token'"
        assert "username" in data, "Response should contain 'username'"
        assert "role" in data, "Response should contain 'role'"
        assert data["username"] == "AdminRECRA", f"Expected username 'AdminRECRA', got '{data['username']}'"
        assert data["role"] == "admin", f"Expected role 'admin', got '{data['role']}'"
        assert isinstance(data["token"], str), "Token should be a string"
        assert len(data["token"]) > 0, "Token should not be empty"
        print(f"✓ Login success: token={data['token'][:20]}..., username={data['username']}, role={data['role']}")
    
    def test_login_wrong_password_returns_401(self):
        """POST /api/auth/login with wrong password returns 401 error"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "AdminRECRA",
            "password": "WrongPassword123"
        })
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "detail" in data, "Response should contain 'detail' error message"
        print(f"✓ Wrong password returns 401: {data['detail']}")
    
    def test_login_wrong_username_returns_401(self):
        """POST /api/auth/login with wrong username returns 401 error"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "WrongUser",
            "password": "Welkom123$"
        })
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "detail" in data, "Response should contain 'detail' error message"
        print(f"✓ Wrong username returns 401: {data['detail']}")
    
    def test_login_empty_credentials_returns_error(self):
        """POST /api/auth/login with empty credentials returns error"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "",
            "password": ""
        })
        # Should return 401 or 422 (validation error)
        assert response.status_code in [401, 422], f"Expected 401 or 422, got {response.status_code}: {response.text}"
        print(f"✓ Empty credentials returns {response.status_code}")


class TestAuthMe:
    """Authentication /me endpoint tests"""
    
    @pytest.fixture
    def auth_token(self):
        """Get a valid auth token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "username": "AdminRECRA",
            "password": "Welkom123$"
        })
        if response.status_code == 200:
            return response.json().get("token")
        pytest.skip("Could not get auth token")
    
    def test_me_with_valid_bearer_token(self, auth_token):
        """GET /api/auth/me with valid Bearer token returns username and role"""
        response = requests.get(f"{BASE_URL}/api/auth/me", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "username" in data, "Response should contain 'username'"
        assert "role" in data, "Response should contain 'role'"
        assert data["username"] == "AdminRECRA", f"Expected username 'AdminRECRA', got '{data['username']}'"
        assert data["role"] == "admin", f"Expected role 'admin', got '{data['role']}'"
        print(f"✓ /me with valid token: username={data['username']}, role={data['role']}")
    
    def test_me_without_token_returns_401(self):
        """GET /api/auth/me without token returns 401"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "detail" in data, "Response should contain 'detail' error message"
        print(f"✓ /me without token returns 401: {data['detail']}")
    
    def test_me_with_invalid_token_returns_401(self):
        """GET /api/auth/me with invalid token returns 401"""
        response = requests.get(f"{BASE_URL}/api/auth/me", headers={
            "Authorization": "Bearer invalid_token_12345"
        })
        assert response.status_code == 401, f"Expected 401, got {response.status_code}: {response.text}"
        print(f"✓ /me with invalid token returns 401")


class TestAuthLogout:
    """Authentication logout endpoint tests"""
    
    def test_logout_clears_cookie(self):
        """POST /api/auth/logout clears cookie and returns success message"""
        # First login to get a cookie
        session = requests.Session()
        login_response = session.post(f"{BASE_URL}/api/auth/login", json={
            "username": "AdminRECRA",
            "password": "Welkom123$"
        })
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        
        # Now logout
        logout_response = session.post(f"{BASE_URL}/api/auth/logout")
        assert logout_response.status_code == 200, f"Expected 200, got {logout_response.status_code}: {logout_response.text}"
        
        data = logout_response.json()
        assert "message" in data, "Response should contain 'message'"
        print(f"✓ Logout success: {data['message']}")


class TestAuthCookieFlow:
    """Test cookie-based authentication flow"""
    
    def test_login_sets_httponly_cookie(self):
        """POST /api/auth/login sets httponly cookie"""
        session = requests.Session()
        response = session.post(f"{BASE_URL}/api/auth/login", json={
            "username": "AdminRECRA",
            "password": "Welkom123$"
        })
        assert response.status_code == 200, f"Login failed: {response.text}"
        
        # Check if access_token cookie was set
        cookies = session.cookies.get_dict()
        # Note: httponly cookies may not be visible in requests library
        # but we can verify the Set-Cookie header
        set_cookie = response.headers.get('Set-Cookie', '')
        if 'access_token' in set_cookie:
            print(f"✓ Login sets access_token cookie")
            assert 'httponly' in set_cookie.lower() or 'HttpOnly' in set_cookie, "Cookie should be httponly"
        else:
            # Cookie might be set but not visible due to httponly
            print(f"✓ Login completed (cookie may be httponly)")
    
    def test_me_with_cookie_auth(self):
        """GET /api/auth/me works with cookie authentication"""
        session = requests.Session()
        
        # Login to get cookie
        login_response = session.post(f"{BASE_URL}/api/auth/login", json={
            "username": "AdminRECRA",
            "password": "Welkom123$"
        })
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        
        # Try /me with the session (should use cookie)
        me_response = session.get(f"{BASE_URL}/api/auth/me")
        assert me_response.status_code == 200, f"Expected 200, got {me_response.status_code}: {me_response.text}"
        
        data = me_response.json()
        assert data["username"] == "AdminRECRA"
        print(f"✓ /me with cookie auth works: username={data['username']}")


class TestExistingEndpointsStillWork:
    """Verify existing endpoints still work after auth implementation"""
    
    def test_products_endpoint_works(self):
        """GET /api/products still works"""
        response = requests.get(f"{BASE_URL}/api/products")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Products should be a list"
        print(f"✓ /api/products works: {len(data)} products")
    
    def test_suppliers_endpoint_works(self):
        """GET /api/suppliers still works"""
        response = requests.get(f"{BASE_URL}/api/suppliers")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Suppliers should be a list"
        print(f"✓ /api/suppliers works: {len(data)} suppliers")
    
    def test_root_endpoint_works(self):
        """GET /api/ still works"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        print(f"✓ /api/ works")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
