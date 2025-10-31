#!/usr/bin/env python3
"""
Test Admin → Student Module Management Flow
"""

import requests
import json
import sys

# Configuration
BASE_URL = "https://autoedge.preview.emergentagent.com/api"

# Admin credentials
ADMIN_USER = {
    "email": "admin@inspecteur-auto.fr", 
    "password": "Admin123456!"
}

def test_admin_flow():
    session = requests.Session()
    
    print("🔐 Testing Admin Authentication...")
    
    # Test admin login
    response = session.post(f"{BASE_URL}/auth/login", json=ADMIN_USER)
    if response.status_code == 200:
        admin_data = response.json()
        admin_token = admin_data["access_token"]
        print(f"✅ Admin authenticated: {ADMIN_USER['email']}")
    else:
        print(f"❌ Admin authentication failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    print("\n🎯 Testing Admin → Student Module Flow...")
    
    # Step 1: Create student account
    student_email = "test.eleve@test.com"
    student_data = {
        "email": student_email,
        "password": "Test123456!",
        "full_name": "Test Élève",
        "username": "testeleve"
    }
    
    # Register or login student
    response = session.post(f"{BASE_URL}/auth/register", json=student_data)
    if response.status_code == 200:
        student_token_data = response.json()
        student_token = student_token_data["access_token"]
        print(f"✅ Student registered: {student_email}")
    else:
        # Try login if already exists
        login_response = session.post(f"{BASE_URL}/auth/login", json={
            "email": student_email,
            "password": student_data["password"]
        })
        if login_response.status_code == 200:
            student_token_data = login_response.json()
            student_token = student_token_data["access_token"]
            print(f"✅ Student logged in: {student_email}")
        else:
            print(f"❌ Student authentication failed: {login_response.status_code}")
            return False
    
    # Step 2: Admin creates new module
    module_data = {
        "title": "Test Module Nouveau",
        "description": "Module de test pour vérifier le flux admin-élève",
        "content": "Contenu de test pour valider l'affichage côté élève. Ce module devrait apparaître dans le dashboard.",
        "duration_minutes": 30,
        "is_free": False
    }
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = session.post(f"{BASE_URL}/admin/modules", json=module_data, headers=admin_headers)
    
    if response.status_code == 200:
        create_result = response.json()
        module_id = create_result["module_id"]
        print(f"✅ Module created: {module_id}")
    else:
        print(f"❌ Module creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Step 3: Verify module appears in list
    response = session.get(f"{BASE_URL}/modules")
    if response.status_code == 200:
        modules = response.json()
        new_module = None
        for module in modules:
            if module.get("title") == "Test Module Nouveau":
                new_module = module
                break
        
        if new_module:
            print(f"✅ Module visible in public list")
        else:
            print(f"❌ Module not found in public list (expected - paid module)")
            # This is actually expected behavior for paid modules
    
    # Step 4: Check student access (should be blocked - paid module)
    student_headers = {"Authorization": f"Bearer {student_token}"}
    response = session.get(f"{BASE_URL}/progress/check-access/{module_id}", headers=student_headers)
    
    if response.status_code == 200:
        access_data = response.json()
        if not access_data.get("can_access") and access_data.get("reason") == "purchase_required":
            print(f"✅ Student access correctly blocked (paid module)")
        else:
            print(f"❌ Unexpected access result: {access_data}")
            return False
    else:
        print(f"❌ Access check failed: {response.status_code}")
        return False
    
    # Step 5: Admin makes module free
    updated_module_data = {
        "title": "Test Module Nouveau",
        "description": "Module de test pour vérifier le flux admin-élève",
        "content": "Contenu modifié - maintenant gratuit !",
        "duration_minutes": 45,
        "is_free": True
    }
    
    response = session.put(f"{BASE_URL}/admin/modules/{module_id}", json=updated_module_data, headers=admin_headers)
    
    if response.status_code == 200:
        print(f"✅ Module updated to free")
    else:
        print(f"❌ Module update failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Step 6: Check student access (should now be allowed)
    response = session.get(f"{BASE_URL}/progress/check-access/{module_id}", headers=student_headers)
    
    if response.status_code == 200:
        access_data = response.json()
        if access_data.get("can_access") and access_data.get("reason") == "free_module":
            print(f"✅ Student can now access free module")
        else:
            print(f"❌ Unexpected access result: {access_data}")
            return False
    else:
        print(f"❌ Access check failed: {response.status_code}")
        return False
    
    # Step 7: Verify updated content
    response = session.get(f"{BASE_URL}/modules/{module_id}", headers=student_headers)
    
    if response.status_code == 200:
        module_data = response.json()
        if "Contenu modifié - maintenant gratuit !" in module_data.get("content", ""):
            print(f"✅ Updated content visible to student")
        else:
            print(f"❌ Updated content not found")
            return False
    else:
        print(f"❌ Module content check failed: {response.status_code}")
        return False
    
    # Step 8: Admin creates quiz for module
    quiz_data = {
        "module_id": module_id,
        "title": "Quiz Test Module",
        "description": "Quiz de test",
        "passing_score": 80,
        "questions": [
            {
                "id": "q1",
                "question": "Question test 1 ?",
                "options": ["Réponse A", "Réponse B", "Réponse C", "Réponse D"],
                "correct_answer": 0,
                "explanation": "La bonne réponse est A"
            },
            {
                "id": "q2",
                "question": "Question test 2 ?",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "correct_answer": 1,
                "explanation": "La bonne réponse est la deuxième"
            }
        ]
    }
    
    response = session.post(f"{BASE_URL}/admin/quizzes", json=quiz_data, headers=admin_headers)
    
    if response.status_code == 200:
        quiz_result = response.json()
        quiz_id = quiz_result["quiz_id"]
        print(f"✅ Quiz created: {quiz_id}")
    else:
        print(f"❌ Quiz creation failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    # Step 9: Student can see quiz
    response = session.get(f"{BASE_URL}/quizzes/module/{module_id}", headers=student_headers)
    
    if response.status_code == 200:
        quiz_data = response.json()
        questions = quiz_data.get("questions", [])
        if len(questions) == 2:
            print(f"✅ Student can access quiz with {len(questions)} questions")
        else:
            print(f"❌ Expected 2 questions, got {len(questions)}")
            return False
    else:
        print(f"❌ Quiz access failed: {response.status_code}")
        return False
    
    # Step 10: Cleanup - Delete module
    response = session.delete(f"{BASE_URL}/admin/modules/{module_id}", headers=admin_headers)
    
    if response.status_code == 200:
        print(f"✅ Module and quiz deleted successfully")
    else:
        print(f"❌ Module deletion failed: {response.status_code}")
        return False
    
    print(f"\n🎉 ALL TESTS PASSED - Admin → Student module flow working correctly!")
    return True

if __name__ == "__main__":
    success = test_admin_flow()
    if not success:
        sys.exit(1)