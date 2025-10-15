#!/usr/bin/env python3
"""
Backend API Testing for Inspecteur Auto Application
Tests all preliminary quiz endpoints and existing module/quiz endpoints
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://mechanic-trainer.preview.emergentagent.com/api"

# Test credentials
TEST_USER = {
    "email": "testuser2@test.com",
    "password": "test123"
}

ADMIN_USER = {
    "email": "admin2@test.com", 
    "password": "admin123"
}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.user_token = None
        self.admin_token = None
        self.test_results = []
        
    def log_test(self, test_name, success, details="", response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        print()
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "response": response_data
        })
    
    def authenticate_user(self):
        """Authenticate test user and get token"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/login", json=TEST_USER)
            if response.status_code == 200:
                data = response.json()
                self.user_token = data["access_token"]
                self.log_test("User Authentication", True, f"Token obtained for {TEST_USER['email']}")
                return True
            else:
                self.log_test("User Authentication", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("User Authentication", False, f"Exception: {str(e)}")
            return False
    
    def authenticate_admin(self):
        """Authenticate admin user and get token"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/login", json=ADMIN_USER)
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data["access_token"]
                self.log_test("Admin Authentication", True, f"Token obtained for {ADMIN_USER['email']}")
                return True
            else:
                self.log_test("Admin Authentication", False, f"Status: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def get_headers(self, use_admin=False):
        """Get authorization headers"""
        token = self.admin_token if use_admin else self.user_token
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    def test_career_fit_quiz_get(self):
        """Test GET /api/preliminary-quiz/career-fit"""
        try:
            response = self.session.get(f"{BASE_URL}/preliminary-quiz/career-fit")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify quiz structure
                required_fields = ["id", "title", "questions"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Career Fit Quiz GET", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check questions count (should be 10)
                questions = data.get("questions", [])
                if len(questions) != 10:
                    self.log_test("Career Fit Quiz GET", False, f"Expected 10 questions, got {len(questions)}")
                    return False
                
                # Verify question structure
                for i, question in enumerate(questions):
                    required_q_fields = ["id", "question", "options", "correct_answer"]
                    missing_q_fields = [field for field in required_q_fields if field not in question]
                    if missing_q_fields:
                        self.log_test("Career Fit Quiz GET", False, f"Question {i+1} missing fields: {missing_q_fields}")
                        return False
                
                self.log_test("Career Fit Quiz GET", True, f"Quiz with {len(questions)} questions retrieved successfully")
                return True
            else:
                self.log_test("Career Fit Quiz GET", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Career Fit Quiz GET", False, f"Exception: {str(e)}")
            return False
    
    def test_career_fit_quiz_submit(self):
        """Test POST /api/preliminary-quiz/career-fit/submit"""
        try:
            # First get the quiz to know the structure
            quiz_response = self.session.get(f"{BASE_URL}/preliminary-quiz/career-fit")
            if quiz_response.status_code != 200:
                self.log_test("Career Fit Quiz Submit", False, "Could not get quiz for submission test")
                return False
            
            quiz_data = quiz_response.json()
            questions = quiz_data.get("questions", [])
            
            # Create answers (mix of correct and incorrect)
            answers = {}
            for i, question in enumerate(questions):
                if i < 7:  # Answer first 7 correctly
                    answers[question["id"]] = question["correct_answer"]
                else:  # Answer last 3 incorrectly
                    correct = question["correct_answer"]
                    # Choose a different answer
                    options_count = len(question.get("options", []))
                    wrong_answer = (correct + 1) % options_count if options_count > 1 else 0
                    answers[question["id"]] = wrong_answer
            
            submission_data = {"answers": answers}
            
            response = self.session.post(f"{BASE_URL}/preliminary-quiz/career-fit/submit", json=submission_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["score", "passed", "correct_answers", "total_questions", "passing_score"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Career Fit Quiz Submit", False, f"Missing response fields: {missing_fields}")
                    return False
                
                # Verify calculations
                expected_correct = 7
                if data["correct_answers"] != expected_correct:
                    self.log_test("Career Fit Quiz Submit", False, f"Expected {expected_correct} correct answers, got {data['correct_answers']}")
                    return False
                
                expected_score = (7 / 10) * 100
                if abs(data["score"] - expected_score) > 0.1:
                    self.log_test("Career Fit Quiz Submit", False, f"Expected score {expected_score}, got {data['score']}")
                    return False
                
                self.log_test("Career Fit Quiz Submit", True, f"Score: {data['score']}%, Passed: {data['passed']}")
                return True
            else:
                self.log_test("Career Fit Quiz Submit", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Career Fit Quiz Submit", False, f"Exception: {str(e)}")
            return False
    
    def test_mechanical_knowledge_quiz_get(self):
        """Test GET /api/preliminary-quiz/mechanical-knowledge"""
        if not self.user_token:
            self.log_test("Mechanical Knowledge Quiz GET", False, "No user token available")
            return False
        
        try:
            headers = self.get_headers()
            response = self.session.get(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify quiz structure
                required_fields = ["id", "title", "questions"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Mechanical Knowledge Quiz GET", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check questions count (should be 12)
                questions = data.get("questions", [])
                if len(questions) != 12:
                    self.log_test("Mechanical Knowledge Quiz GET", False, f"Expected 12 questions, got {len(questions)}")
                    return False
                
                self.log_test("Mechanical Knowledge Quiz GET", True, f"Quiz with {len(questions)} questions retrieved successfully")
                return True
            else:
                self.log_test("Mechanical Knowledge Quiz GET", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Mechanical Knowledge Quiz GET", False, f"Exception: {str(e)}")
            return False
    
    def test_mechanical_knowledge_quiz_submit_failing(self):
        """Test POST /api/preliminary-quiz/mechanical-knowledge/submit with failing score"""
        if not self.user_token:
            self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, "No user token available")
            return False
        
        try:
            # First get the quiz
            headers = self.get_headers()
            quiz_response = self.session.get(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge", headers=headers)
            if quiz_response.status_code != 200:
                self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, "Could not get quiz for submission test")
                return False
            
            quiz_data = quiz_response.json()
            questions = quiz_data.get("questions", [])
            
            # Create answers for failing score (< 70%)
            answers = {}
            for i, question in enumerate(questions):
                if i < 6:  # Answer first 6 correctly (50%)
                    answers[question["id"]] = question["correct_answer"]
                else:  # Answer rest incorrectly
                    correct = question["correct_answer"]
                    options_count = len(question.get("options", []))
                    wrong_answer = (correct + 1) % options_count if options_count > 1 else 0
                    answers[question["id"]] = wrong_answer
            
            submission_data = {"answers": answers}
            
            response = self.session.post(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge/submit", json=submission_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["score", "passed", "needs_remedial_module", "correct_answers", "total_questions"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, f"Missing response fields: {missing_fields}")
                    return False
                
                # Verify failing score logic
                if data["score"] >= 70:
                    self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, f"Expected failing score < 70%, got {data['score']}%")
                    return False
                
                if not data["needs_remedial_module"]:
                    self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, "Expected needs_remedial_module=true for failing score")
                    return False
                
                if data["passed"]:
                    self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, "Expected passed=false for failing score")
                    return False
                
                self.log_test("Mechanical Knowledge Quiz Submit (Failing)", True, f"Score: {data['score']}%, Needs remedial: {data['needs_remedial_module']}")
                return True
            else:
                self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Mechanical Knowledge Quiz Submit (Failing)", False, f"Exception: {str(e)}")
            return False
    
    def test_mechanical_knowledge_quiz_submit_passing(self):
        """Test POST /api/preliminary-quiz/mechanical-knowledge/submit with passing score"""
        if not self.user_token:
            self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, "No user token available")
            return False
        
        try:
            # First get the quiz
            headers = self.get_headers()
            quiz_response = self.session.get(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge", headers=headers)
            if quiz_response.status_code != 200:
                self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, "Could not get quiz for submission test")
                return False
            
            quiz_data = quiz_response.json()
            questions = quiz_data.get("questions", [])
            
            # Create answers for passing score (>= 70%)
            answers = {}
            for i, question in enumerate(questions):
                if i < 9:  # Answer first 9 correctly (75%)
                    answers[question["id"]] = question["correct_answer"]
                else:  # Answer rest incorrectly
                    correct = question["correct_answer"]
                    options_count = len(question.get("options", []))
                    wrong_answer = (correct + 1) % options_count if options_count > 1 else 0
                    answers[question["id"]] = wrong_answer
            
            submission_data = {"answers": answers}
            
            response = self.session.post(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge/submit", json=submission_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify passing score logic
                if data["score"] < 70:
                    self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, f"Expected passing score >= 70%, got {data['score']}%")
                    return False
                
                if data["needs_remedial_module"]:
                    self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, "Expected needs_remedial_module=false for passing score")
                    return False
                
                if not data["passed"]:
                    self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, "Expected passed=true for passing score")
                    return False
                
                self.log_test("Mechanical Knowledge Quiz Submit (Passing)", True, f"Score: {data['score']}%, Needs remedial: {data['needs_remedial_module']}")
                return True
            else:
                self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Mechanical Knowledge Quiz Submit (Passing)", False, f"Exception: {str(e)}")
            return False
    
    def test_mechanical_knowledge_status(self):
        """Test GET /api/preliminary-quiz/mechanical-knowledge/status"""
        if not self.user_token:
            self.log_test("Mechanical Knowledge Status", False, "No user token available")
            return False
        
        try:
            headers = self.get_headers()
            response = self.session.get(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge/status", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["completed", "needs_remedial_module", "score"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Mechanical Knowledge Status", False, f"Missing response fields: {missing_fields}")
                    return False
                
                self.log_test("Mechanical Knowledge Status", True, f"Completed: {data['completed']}, Score: {data['score']}")
                return True
            else:
                self.log_test("Mechanical Knowledge Status", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Mechanical Knowledge Status", False, f"Exception: {str(e)}")
            return False
    
    def test_modules_list(self):
        """Test GET /api/modules"""
        try:
            headers = self.get_headers() if self.user_token else {}
            response = self.session.get(f"{BASE_URL}/modules", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    self.log_test("Modules List", False, "Expected list of modules")
                    return False
                
                # Should have 8 modules
                if len(data) < 8:
                    self.log_test("Modules List", False, f"Expected at least 8 modules, got {len(data)}")
                    return False
                
                # Check if Module 2 exists (Remise à Niveau Mécanique)
                module_2_found = False
                for module in data:
                    if module.get("order_index") == 2:
                        module_2_found = True
                        if "Remise à Niveau" not in module.get("title", ""):
                            self.log_test("Modules List", False, f"Module 2 title doesn't contain 'Remise à Niveau': {module.get('title')}")
                            return False
                        break
                
                if not module_2_found:
                    self.log_test("Modules List", False, "Module 2 (Remise à Niveau Mécanique) not found")
                    return False
                
                self.log_test("Modules List", True, f"Retrieved {len(data)} modules, Module 2 found")
                return True
            else:
                self.log_test("Modules List", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Modules List", False, f"Exception: {str(e)}")
            return False
    
    def test_module_quiz_free(self):
        """Test GET /api/quizzes/module/{module_id} for free module"""
        try:
            # First get modules to find a free one
            headers = self.get_headers() if self.user_token else {}
            modules_response = self.session.get(f"{BASE_URL}/modules", headers=headers)
            
            if modules_response.status_code != 200:
                self.log_test("Module Quiz (Free)", False, "Could not get modules list")
                return False
            
            modules = modules_response.json()
            free_module = None
            for module in modules:
                if module.get("is_free", False):
                    free_module = module
                    break
            
            if not free_module:
                self.log_test("Module Quiz (Free)", False, "No free module found")
                return False
            
            # Get quiz for free module
            response = self.session.get(f"{BASE_URL}/quizzes/module/{free_module['id']}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ["id", "module_id", "title", "questions"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Module Quiz (Free)", False, f"Missing fields: {missing_fields}")
                    return False
                
                self.log_test("Module Quiz (Free)", True, f"Quiz for free module '{free_module['title']}' retrieved")
                return True
            else:
                self.log_test("Module Quiz (Free)", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Module Quiz (Free)", False, f"Exception: {str(e)}")
            return False
    
    def test_module_quiz_paid_no_purchase(self):
        """Test GET /api/quizzes/module/{module_id} for paid module without purchase"""
        try:
            # First get modules to find a paid one
            modules_response = self.session.get(f"{BASE_URL}/modules")
            
            if modules_response.status_code != 200:
                self.log_test("Module Quiz (Paid - No Purchase)", False, "Could not get modules list")
                return False
            
            modules = modules_response.json()
            paid_module = None
            for module in modules:
                if not module.get("is_free", False):
                    paid_module = module
                    break
            
            if not paid_module:
                self.log_test("Module Quiz (Paid - No Purchase)", False, "No paid module found")
                return False
            
            # Try to get quiz for paid module without authentication or purchase
            response = self.session.get(f"{BASE_URL}/quizzes/module/{paid_module['id']}")
            
            if response.status_code == 403:
                self.log_test("Module Quiz (Paid - No Purchase)", True, "Correctly blocked access to paid module quiz")
                return True
            elif response.status_code == 401:
                self.log_test("Module Quiz (Paid - No Purchase)", True, "Correctly requires authentication for paid module quiz")
                return True
            else:
                self.log_test("Module Quiz (Paid - No Purchase)", False, f"Expected 403/401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Module Quiz (Paid - No Purchase)", False, f"Exception: {str(e)}")
            return False
    
    def test_quiz_submission(self):
        """Test POST /api/quizzes/{quiz_id}/submit"""
        if not self.user_token:
            self.log_test("Quiz Submission", False, "No user token available")
            return False
        
        try:
            # Get a free module quiz first
            headers = self.get_headers()
            modules_response = self.session.get(f"{BASE_URL}/modules", headers=headers)
            
            if modules_response.status_code != 200:
                self.log_test("Quiz Submission", False, "Could not get modules list")
                return False
            
            modules = modules_response.json()
            free_module = None
            for module in modules:
                if module.get("is_free", False):
                    free_module = module
                    break
            
            if not free_module:
                self.log_test("Quiz Submission", False, "No free module found")
                return False
            
            # Get the quiz
            quiz_response = self.session.get(f"{BASE_URL}/quizzes/module/{free_module['id']}", headers=headers)
            if quiz_response.status_code != 200:
                self.log_test("Quiz Submission", False, "Could not get quiz")
                return False
            
            quiz_data = quiz_response.json()
            questions = quiz_data.get("questions", [])
            
            # Create answers
            answers = {}
            for question in questions:
                answers[question["id"]] = question["correct_answer"]
            
            submission_data = {"answers": answers}
            
            response = self.session.post(f"{BASE_URL}/quizzes/{quiz_data['id']}/submit", json=submission_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ["score", "passed", "correct_answers", "total_questions"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Quiz Submission", False, f"Missing response fields: {missing_fields}")
                    return False
                
                self.log_test("Quiz Submission", True, f"Quiz submitted successfully, Score: {data['score']}%")
                return True
            else:
                self.log_test("Quiz Submission", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Quiz Submission", False, f"Exception: {str(e)}")
            return False
    
    def test_authentication_errors(self):
        """Test authentication error handling"""
        try:
            # Test mechanical knowledge quiz without auth
            response = self.session.get(f"{BASE_URL}/preliminary-quiz/mechanical-knowledge")
            
            if response.status_code == 401:
                self.log_test("Authentication Error Handling", True, "Correctly requires authentication for mechanical knowledge quiz")
                return True
            else:
                self.log_test("Authentication Error Handling", False, f"Expected 401, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Authentication Error Handling", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests in order"""
        print("=" * 80)
        print("INSPECTEUR AUTO BACKEND API TESTING")
        print("=" * 80)
        print()
        
        # Authentication tests
        print("🔐 AUTHENTICATION TESTS")
        print("-" * 40)
        user_auth_success = self.authenticate_user()
        admin_auth_success = self.authenticate_admin()
        print()
        
        # Priority 1: Preliminary Quiz Endpoints
        print("🎯 PRIORITY 1: PRELIMINARY QUIZ ENDPOINTS")
        print("-" * 50)
        
        # Career fit quiz (no auth required)
        self.test_career_fit_quiz_get()
        self.test_career_fit_quiz_submit()
        
        # Mechanical knowledge quiz (auth required)
        if user_auth_success:
            self.test_mechanical_knowledge_quiz_get()
            self.test_mechanical_knowledge_quiz_submit_failing()
            self.test_mechanical_knowledge_quiz_submit_passing()
            self.test_mechanical_knowledge_status()
        
        print()
        
        # Priority 2: Existing Module & Quiz Endpoints
        print("📚 PRIORITY 2: MODULE & QUIZ ENDPOINTS")
        print("-" * 45)
        
        self.test_modules_list()
        self.test_module_quiz_free()
        self.test_module_quiz_paid_no_purchase()
        
        if user_auth_success:
            self.test_quiz_submission()
        
        print()
        
        # Error handling tests
        print("⚠️  ERROR HANDLING TESTS")
        print("-" * 30)
        self.test_authentication_errors()
        
        print()
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            print("-" * 20)
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test']}: {result['details']}")
            print()
        
        # Critical issues
        critical_issues = []
        
        # Check for critical preliminary quiz issues
        prelim_tests = [r for r in self.test_results if "preliminary-quiz" in r["test"].lower() or "career fit" in r["test"].lower() or "mechanical knowledge" in r["test"].lower()]
        failed_prelim = [r for r in prelim_tests if not r["success"]]
        
        if failed_prelim:
            critical_issues.append(f"Preliminary quiz endpoints failing: {len(failed_prelim)}/{len(prelim_tests)} tests failed")
        
        # Check for authentication issues
        auth_tests = [r for r in self.test_results if "authentication" in r["test"].lower()]
        failed_auth = [r for r in auth_tests if not r["success"]]
        
        if failed_auth:
            critical_issues.append("Authentication system not working properly")
        
        if critical_issues:
            print("🚨 CRITICAL ISSUES:")
            print("-" * 20)
            for issue in critical_issues:
                print(f"• {issue}")
            print()
        
        return failed_tests == 0

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    
    if not success:
        sys.exit(1)