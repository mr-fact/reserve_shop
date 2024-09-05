import unittest
from unittest import mock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.postgresql import Base, get_db
from main import app  # Replace with the actual import of your FastAPI app

# Set up a testing database (SQLite in-memory for simplicity)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create tables in the testing database
        Base.metadata.create_all(bind=engine)

        # Override the get_db dependency to use the testing database
        def override_get_db():
            try:
                db = TestingSessionLocal()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Drop tables in the testing database
        Base.metadata.drop_all(bind=engine)

    def __init__(self, *args, **kwargs):
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI1NDYzMTE0LCJpYXQiOjE3MjUzNzY3MTQsImp0aSI6ImRiYjFlYjBjLWQzNDctNDQ5YS1hZGU3LTI2MWMyYzRiOGU2YyIsInVzZXJfaWQiOiI3In0.f0asPxJp9jPMPTFjMwKGoAUxR4an5cQBBMvFzXTEmgBbN6StYV3fiGPuTN_vfkUxW2tGc8gu_wH_6QQQqX3cybpQhWdfN8tiJ-Ad8xObNasdKLvjQvkFcQK7_NLY4oK7SWSdT5H1Z1hw_PhSpZ7-PpHQDt7F3J4pvhdCSqJ-wnawNCUJ_UEGQMAi1uZolQKDeM63gBVhFXMXINGWDYPxGLauhe-Cuy_nBiHWX4kF3JBs50cwqLUZudpXhWr_DSYIAhRtA-ImMeMEN97VEwzaWFUlbc7kSMqtVlS9FPoMYmPjM_08Ozo_BED28OJ0Xm94X3zboGp4cn50I5AF22-0GA'
        self.otp = '1123'
        super().__init__(*args, **kwargs)

    def test_send_otp(self):
        response = self.client.post('/auth/send-otp/', json={"phone": "+989112223344"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())
        self.assertIn('otp', response.json())

    def test_verify_otp_success(self):
        with unittest.mock.patch('services.verify_otp', return_value=(True, "Success")):
            with unittest.mock.patch('services.get_or_create_user', return_value={"phone": "+989112223344"}):
                with unittest.mock.patch('services.create_access_token', return_value=self.token):
                    response = self.client.post('/auth/verify-otp/', json={"phone": "+989112223344", "otp_code": self.otp})
                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(response.json()['result'])
                    self.assertEqual(response.json()['message'], "Success")
                    self.assertIn('token', response.json())

    def test_verify_otp_failure(self):
        with unittest.mock.patch('services.verify_otp', return_value=(False, "Invalid OTP")):
            response = self.client.post('/auth/verify-otp/', json={"phone": "+989112223344", "otp_code": "9238"})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json()['detail'], "Invalid OTP")

    def test_get_user_information(self):
        response = self.client.get('/auth/user/me/', headers={"Authorization": f"{self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone', response.json())
        self.assertEqual(response.json()['phone'], "+989112223344")

    def test_update_user_information(self):
        response = self.client.patch('/auth/user/me/', json={"phone": "+989112223344", "name": "new name"},
                                     headers={"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('phone', response.json())
        self.assertEqual(response.json()['phone'], "+989112223344")
        self.assertEqual(response.json()['name'], "new name")

    def test_get_user_information_by_phone(self):
        with unittest.mock.patch('services.get_user', return_value={"phone": "+989112223344"}):
            response = self.client.get('/auth/user/+989112223344/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('phone', response.json())
            self.assertEqual(response.json()['phone'], "+989112223344")

    def test_get_user_information_by_phone_not_found(self):
        with unittest.mock.patch('services.get_user', return_value=None):
            response = self.client.get('/auth/user/+989112223345/')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json()['detail'], 'not found')
