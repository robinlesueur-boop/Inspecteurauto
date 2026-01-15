"""
Backend API Tests for Private Chat System (Élève-Admin)
Tests: Chat endpoints, WebSocket, message sending/receiving
"""
import pytest
import requests
import os
import uuid
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://autoinspect-fix.preview.emergentagent.com')

# Test credentials
ADMIN_EMAIL = "admin@inspecteur-auto.fr"
ADMIN_PASSWORD = "Admin123!"
STUDENT_EMAIL = "eleve.test@inspecteur-auto.fr"
STUDENT_PASSWORD = "Eleve123!"


class TestChatAuthentication:
    """Test authentication for chat endpoints"""
    
    def test_student_login(self):
        """Test student login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        assert response.status_code == 200, f"Student login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == STUDENT_EMAIL
        print(f"Student login successful: {STUDENT_EMAIL}")
        print(f"Student has_purchased: {data['user'].get('has_purchased', False)}")
        return data
    
    def test_admin_login(self):
        """Test admin login with valid credentials"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        assert response.status_code == 200, f"Admin login failed: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert data["user"]["is_admin"] == True
        print(f"Admin login successful: {ADMIN_EMAIL}")
        return data


class TestStudentChatEndpoints:
    """Test student chat endpoints"""
    
    @pytest.fixture
    def student_token(self):
        """Get student authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Student authentication failed")
    
    @pytest.fixture
    def student_user(self):
        """Get student user data"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["user"]
        pytest.skip("Student authentication failed")
    
    def test_get_chat_messages_student(self, student_token, student_user):
        """Test GET /api/chat/messages for student"""
        # Check if student has purchased
        if not student_user.get("has_purchased", False):
            pytest.skip("Student has not purchased - chat access requires purchase")
        
        response = requests.get(
            f"{BASE_URL}/api/chat/messages",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200, f"Get messages failed: {response.text}"
        data = response.json()
        assert isinstance(data, list)
        print(f"Student has {len(data)} messages in chat")
        
        # Verify message structure if messages exist
        if len(data) > 0:
            msg = data[0]
            assert "id" in msg
            assert "content" in msg
            assert "sender_type" in msg
            assert "created_at" in msg
            print(f"First message: {msg['content'][:50]}... (from {msg['sender_type']})")
        
        return data
    
    def test_send_chat_message_student(self, student_token, student_user):
        """Test POST /api/chat/messages for student"""
        if not student_user.get("has_purchased", False):
            pytest.skip("Student has not purchased - chat access requires purchase")
        
        unique_content = f"Test message from student - {uuid.uuid4().hex[:8]}"
        
        response = requests.post(
            f"{BASE_URL}/api/chat/messages",
            json={"content": unique_content},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200, f"Send message failed: {response.text}"
        data = response.json()
        assert "message" in data
        assert "id" in data
        print(f"Message sent successfully: {data['id']}")
        
        # Verify message appears in chat
        time.sleep(0.5)  # Small delay for DB write
        get_response = requests.get(
            f"{BASE_URL}/api/chat/messages",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert get_response.status_code == 200
        messages = get_response.json()
        
        # Find our message
        found = any(m.get("content") == unique_content for m in messages)
        assert found, "Sent message not found in chat history"
        print("Message verified in chat history")
        
        return data
    
    def test_get_chat_conversation_student(self, student_token, student_user):
        """Test GET /api/chat/conversation for student"""
        if not student_user.get("has_purchased", False):
            pytest.skip("Student has not purchased - chat access requires purchase")
        
        response = requests.get(
            f"{BASE_URL}/api/chat/conversation",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200, f"Get conversation failed: {response.text}"
        data = response.json()
        
        # Verify conversation structure
        assert "id" in data
        assert "student_id" in data
        print(f"Conversation ID: {data['id']}")
        print(f"Unread by student: {data.get('unread_by_student', 0)}")
        
        return data
    
    def test_get_unread_count_student(self, student_token, student_user):
        """Test GET /api/chat/unread-count for student"""
        if not student_user.get("has_purchased", False):
            pytest.skip("Student has not purchased - chat access requires purchase")
        
        response = requests.get(
            f"{BASE_URL}/api/chat/unread-count",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200, f"Get unread count failed: {response.text}"
        data = response.json()
        assert "unread" in data
        print(f"Unread messages for student: {data['unread']}")
        
        return data
    
    def test_chat_access_without_purchase(self):
        """Test that chat access is denied without purchase"""
        # Create a new user without purchase
        unique_email = f"test_nopurchase_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register new user
        register_response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "email": unique_email,
            "username": f"testuser_{uuid.uuid4().hex[:6]}",
            "full_name": "Test No Purchase",
            "password": "TestPass123!"
        })
        
        if register_response.status_code != 200:
            pytest.skip("Could not create test user")
        
        token = register_response.json()["access_token"]
        
        # Try to access chat
        response = requests.get(
            f"{BASE_URL}/api/chat/messages",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # Should be 403 Forbidden
        assert response.status_code == 403, f"Expected 403, got {response.status_code}: {response.text}"
        print("Chat access correctly denied for non-premium user")
    
    def test_send_empty_message(self, student_token, student_user):
        """Test that empty messages are rejected"""
        if not student_user.get("has_purchased", False):
            pytest.skip("Student has not purchased - chat access requires purchase")
        
        response = requests.post(
            f"{BASE_URL}/api/chat/messages",
            json={"content": ""},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Should be 400 Bad Request
        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
        print("Empty message correctly rejected")


class TestAdminChatEndpoints:
    """Test admin chat endpoints"""
    
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
    
    def test_get_all_conversations_admin(self, admin_token):
        """Test GET /api/admin/chat/conversations"""
        response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"Get conversations failed: {response.text}"
        data = response.json()
        assert isinstance(data, list)
        print(f"Admin sees {len(data)} conversations")
        
        # Verify conversation structure if any exist
        if len(data) > 0:
            conv = data[0]
            assert "id" in conv
            assert "student_id" in conv
            assert "student_name" in conv
            assert "student_email" in conv
            print(f"First conversation: {conv['student_name']} ({conv['student_email']})")
            print(f"Unread by admin: {conv.get('unread_by_admin', 0)}")
        
        return data
    
    def test_get_conversation_messages_admin(self, admin_token):
        """Test GET /api/admin/chat/conversations/{id}/messages"""
        # First get conversations
        conv_response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert conv_response.status_code == 200
        conversations = conv_response.json()
        
        if len(conversations) == 0:
            pytest.skip("No conversations available to test")
        
        conv_id = conversations[0]["id"]
        
        # Get messages for this conversation
        response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations/{conv_id}/messages",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"Get messages failed: {response.text}"
        data = response.json()
        assert isinstance(data, list)
        print(f"Conversation {conv_id} has {len(data)} messages")
        
        # Verify message structure
        if len(data) > 0:
            msg = data[0]
            assert "id" in msg
            assert "content" in msg
            assert "sender_type" in msg
            assert "created_at" in msg
            print(f"First message: {msg['content'][:50]}... (from {msg['sender_type']})")
        
        return data
    
    def test_admin_send_message(self, admin_token):
        """Test POST /api/admin/chat/conversations/{id}/messages"""
        # First get conversations
        conv_response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert conv_response.status_code == 200
        conversations = conv_response.json()
        
        if len(conversations) == 0:
            pytest.skip("No conversations available to test")
        
        conv_id = conversations[0]["id"]
        unique_content = f"Admin reply - {uuid.uuid4().hex[:8]}"
        
        # Send message
        response = requests.post(
            f"{BASE_URL}/api/admin/chat/conversations/{conv_id}/messages",
            json={"content": unique_content},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"Send message failed: {response.text}"
        data = response.json()
        assert "message" in data
        assert "id" in data
        print(f"Admin message sent: {data['id']}")
        
        # Verify message appears
        time.sleep(0.5)
        get_response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations/{conv_id}/messages",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert get_response.status_code == 200
        messages = get_response.json()
        
        found = any(m.get("content") == unique_content for m in messages)
        assert found, "Admin message not found in conversation"
        print("Admin message verified in conversation")
        
        return data
    
    def test_get_unread_total_admin(self, admin_token):
        """Test GET /api/admin/chat/unread-total"""
        response = requests.get(
            f"{BASE_URL}/api/admin/chat/unread-total",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200, f"Get unread total failed: {response.text}"
        data = response.json()
        assert "unread" in data
        print(f"Total unread messages for admin: {data['unread']}")
        
        return data
    
    def test_admin_endpoints_require_admin(self):
        """Test that admin chat endpoints require admin role"""
        # Login as student
        student_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        
        if student_response.status_code != 200:
            pytest.skip("Student login failed")
        
        student_token = student_response.json()["access_token"]
        
        # Try to access admin conversations
        response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print("Admin chat endpoints correctly require admin role")
    
    def test_get_nonexistent_conversation(self, admin_token):
        """Test getting messages for non-existent conversation"""
        fake_id = str(uuid.uuid4())
        
        response = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations/{fake_id}/messages",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"
        print("Non-existent conversation correctly returns 404")


class TestChatIntegration:
    """Integration tests for chat flow"""
    
    @pytest.fixture
    def student_token(self):
        """Get student authentication token"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        pytest.skip("Student authentication failed")
    
    @pytest.fixture
    def student_user(self):
        """Get student user data"""
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": STUDENT_EMAIL,
            "password": STUDENT_PASSWORD
        })
        if response.status_code == 200:
            return response.json()["user"]
        pytest.skip("Student authentication failed")
    
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
    
    def test_full_chat_flow(self, student_token, student_user, admin_token):
        """Test complete chat flow: student sends, admin sees, admin replies"""
        if not student_user.get("has_purchased", False):
            pytest.skip("Student has not purchased - chat access requires purchase")
        
        # Step 1: Student sends a message
        unique_content = f"Integration test message - {uuid.uuid4().hex[:8]}"
        
        student_send = requests.post(
            f"{BASE_URL}/api/chat/messages",
            json={"content": unique_content},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert student_send.status_code == 200, f"Student send failed: {student_send.text}"
        print(f"Step 1: Student sent message")
        
        time.sleep(0.5)
        
        # Step 2: Admin sees the conversation
        admin_convs = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert admin_convs.status_code == 200
        conversations = admin_convs.json()
        
        # Find conversation with our student
        student_conv = next(
            (c for c in conversations if c.get("student_email") == STUDENT_EMAIL),
            None
        )
        assert student_conv is not None, "Student conversation not found by admin"
        print(f"Step 2: Admin found student conversation: {student_conv['id']}")
        
        # Step 3: Admin sees the message
        admin_msgs = requests.get(
            f"{BASE_URL}/api/admin/chat/conversations/{student_conv['id']}/messages",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert admin_msgs.status_code == 200
        messages = admin_msgs.json()
        
        found_msg = any(m.get("content") == unique_content for m in messages)
        assert found_msg, "Student message not visible to admin"
        print(f"Step 3: Admin can see student message")
        
        # Step 4: Admin replies
        admin_reply = f"Admin reply to integration test - {uuid.uuid4().hex[:8]}"
        
        admin_send = requests.post(
            f"{BASE_URL}/api/admin/chat/conversations/{student_conv['id']}/messages",
            json={"content": admin_reply},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert admin_send.status_code == 200, f"Admin send failed: {admin_send.text}"
        print(f"Step 4: Admin sent reply")
        
        time.sleep(0.5)
        
        # Step 5: Student sees admin reply
        student_msgs = requests.get(
            f"{BASE_URL}/api/chat/messages",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        assert student_msgs.status_code == 200
        student_messages = student_msgs.json()
        
        found_reply = any(m.get("content") == admin_reply for m in student_messages)
        assert found_reply, "Admin reply not visible to student"
        print(f"Step 5: Student can see admin reply")
        
        print("✅ Full chat flow integration test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
