"""
Backend API Tests for Inspecteur Auto Platform
Tests: Authentication, Pre-registration, Admin endpoints
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://autoinspect-fix.preview.emergentagent.com')

# Test credentials
ADMIN_EMAIL = "admin@inspecteur-auto.fr"
ADMIN_PASSWORD = "Admin123!"


class TestHealthAndBasicEndpoints:
    """Basic health and public endpoint tests"""
    
    def test_modules_all_public(self):
        """Test public modules endpoint"""
        response = requests.get(f"{BASE_URL}/api/modules/all-public")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Found {len(data)} public modules")
    

class TestAuthentication:
    """Authentication endpoint tests"""
    
    def test_login_success(self):
        """Test admin login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == ADMIN_EMAIL
        assert data["user"]["is_admin"] == True
        print(f"Login successful for {ADMIN_EMAIL}")
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print("Invalid credentials correctly rejected")
    
    def test_auth_me_with_token(self):
        """Test /auth/me endpoint with valid token"""
        # First login
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Then check /auth/me
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == ADMIN_EMAIL
        print("Auth/me endpoint works correctly")
    
    def test_auth_me_without_token(self):
        """Test /auth/me endpoint without token"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code in [401, 403]
        print("Auth/me correctly rejects unauthenticated requests")


class TestPreRegistration:
    """Pre-registration questionnaire tests"""
    
    def test_submit_pre_registration_with_phone(self):
        """Test pre-registration submission with phone number"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        response = requests.post(f"{BASE_URL}/api/pre-registration/submit", json={
            "email": unique_email,
            "full_name": "Test User",
            "phone": "0612345678",
            "answers": {
                "q1": "oui_pro",
                "q2": "expert",
                "q3": "independant",
                "q4": "immediat",
                "q5": "souvent",
                "q6": "tres",
                "q7": "salarie",
                "q8": "10plus",
                "q9": "oui_complet",
                "q10": "independance"
            },
            "has_driving_license": True
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["validated"] == True
        assert "questionnaire_id" in data
        print(f"Pre-registration submitted successfully: {data['questionnaire_id']}")
        return data["questionnaire_id"]
    
    def test_submit_pre_registration_without_phone(self):
        """Test pre-registration fails without phone number"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        response = requests.post(f"{BASE_URL}/api/pre-registration/submit", json={
            "email": unique_email,
            "full_name": "Test User",
            "phone": "",  # Empty phone
            "answers": {
                "q1": "oui_pro",
                "q2": "expert",
                "q3": "independant",
                "q4": "immediat",
                "q5": "souvent",
                "q6": "tres",
                "q7": "salarie",
                "q8": "10plus",
                "q9": "oui_complet",
                "q10": "independance"
            },
            "has_driving_license": True
        })
        
        assert response.status_code == 400
        print("Pre-registration correctly rejects empty phone")
    
    def test_submit_pre_registration_without_license(self):
        """Test pre-registration fails without driving license"""
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        response = requests.post(f"{BASE_URL}/api/pre-registration/submit", json={
            "email": unique_email,
            "full_name": "Test User",
            "phone": "0612345678",
            "answers": {
                "q1": "oui_pro",
                "q2": "expert",
                "q3": "independant",
                "q4": "immediat",
                "q5": "souvent",
                "q6": "tres",
                "q7": "salarie",
                "q8": "10plus",
                "q9": "oui_complet",
                "q10": "independance"
            },
            "has_driving_license": False  # No license
        })
        
        assert response.status_code == 400
        print("Pre-registration correctly rejects without driving license")


class TestAdminPreRegistrations:
    """Admin pre-registration management tests"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Admin authentication failed")
    
    def test_get_pre_registrations(self, admin_token):
        """Test getting all pre-registrations as admin"""
        response = requests.get(
            f"{BASE_URL}/api/admin/pre-registrations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"Found {len(data)} pre-registrations")
        
        # Verify data structure
        if len(data) > 0:
            prospect = data[0]
            assert "id" in prospect
            assert "email" in prospect
            assert "full_name" in prospect
            print(f"First prospect: {prospect['full_name']} - {prospect['email']}")
    
    def test_get_pre_registrations_unauthorized(self):
        """Test pre-registrations endpoint without admin token"""
        response = requests.get(f"{BASE_URL}/api/admin/pre-registrations")
        assert response.status_code in [401, 403]
        print("Pre-registrations correctly rejects unauthenticated requests")
    
    def test_update_callback_status(self, admin_token):
        """Test updating prospect callback status"""
        # First create a new prospect
        unique_email = f"test_callback_{uuid.uuid4().hex[:8]}@example.com"
        
        create_response = requests.post(f"{BASE_URL}/api/pre-registration/submit", json={
            "email": unique_email,
            "full_name": "Test Prospect",
            "phone": "0612345678",
            "answers": {
                "q1": "oui_pro",
                "q2": "expert",
                "q3": "independant",
                "q4": "immediat",
                "q5": "souvent",
                "q6": "tres",
                "q7": "salarie",
                "q8": "10plus",
                "q9": "oui_complet",
                "q10": "independance"
            },
            "has_driving_license": True
        })
        
        assert create_response.status_code == 200
        prospect_id = create_response.json()["questionnaire_id"]
        print(f"Created prospect: {prospect_id}")
        
        # Update callback status
        update_response = requests.patch(
            f"{BASE_URL}/api/admin/pre-registrations/{prospect_id}/callback",
            json={
                "callback_status": "called",
                "callback_notes": "Appelé, très intéressé par la formation"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert update_response.status_code == 200
        print(f"Callback status updated for prospect {prospect_id}")
        
        # Verify the update by fetching all prospects
        get_response = requests.get(
            f"{BASE_URL}/api/admin/pre-registrations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert get_response.status_code == 200
        prospects = get_response.json()
        
        # Find our prospect
        updated_prospect = next((p for p in prospects if p["id"] == prospect_id), None)
        assert updated_prospect is not None
        assert updated_prospect["callback_status"] == "called"
        assert updated_prospect["callback_notes"] == "Appelé, très intéressé par la formation"
        print(f"Verified callback status update: {updated_prospect['callback_status']}")
    
    def test_update_callback_invalid_status(self, admin_token):
        """Test updating with invalid callback status"""
        # First create a prospect
        unique_email = f"test_invalid_{uuid.uuid4().hex[:8]}@example.com"
        
        create_response = requests.post(f"{BASE_URL}/api/pre-registration/submit", json={
            "email": unique_email,
            "full_name": "Test Invalid",
            "phone": "0612345678",
            "answers": {
                "q1": "oui_pro",
                "q2": "expert",
                "q3": "independant",
                "q4": "immediat",
                "q5": "souvent",
                "q6": "tres",
                "q7": "salarie",
                "q8": "10plus",
                "q9": "oui_complet",
                "q10": "independance"
            },
            "has_driving_license": True
        })
        
        prospect_id = create_response.json()["questionnaire_id"]
        
        # Try invalid status
        update_response = requests.patch(
            f"{BASE_URL}/api/admin/pre-registrations/{prospect_id}/callback",
            json={
                "callback_status": "invalid_status",
                "callback_notes": "Test"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert update_response.status_code == 400
        print("Invalid callback status correctly rejected")


class TestModulesEndpoints:
    """Module-related endpoint tests"""
    
    def test_get_all_public_modules(self):
        """Test getting all public modules"""
        response = requests.get(f"{BASE_URL}/api/modules/all-public")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Verify module structure
        if len(data) > 0:
            module = data[0]
            assert "id" in module
            assert "title" in module
            assert "description" in module
            assert "order_index" in module
            assert "is_free" in module
            print(f"First module: {module['title']} (order: {module['order_index']})")
        
        print(f"Total public modules: {len(data)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
