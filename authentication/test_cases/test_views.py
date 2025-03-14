from .test_setup import TestSetup
import pdb

class TestViews(TestSetup):

    def testUserSignup(self):
        """
        Test user can sign up successfully
        """
        res = self.client.post(self.signup_url, {
            "username": "newguy",
            "password": "Pass1234!",
            "confirm_password": "Pass1234!"
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("token", res.json())

    def testUserCantSignupWithNoData(self):
        """
        Test that a user cannot sign up with incomplete data
        """
        res = self.client.post(self.signup_url, {}, format="json")
        self.assertEqual(res.status_code, 400)

    def testUserCantSignupWithExistingUsername(self):
        """
        Test that a user cannot sign up with an already taken username
        """
        self.client.post(self.signup_url, self.user_data, format="json")  # Create user first
        res = self.client.post(self.signup_url, self.user_data, format="json")  # Try again
        self.assertEqual(res.status_code, 400)

    def testUserCantSignupWithWeakPassword(self):
        """
        Test that a user cannot sign up with a weak password
        """
        res = self.client.post(self.signup_url, {
            "username": "weakpassworduser",
            "password": "123"
        }, format="json")
        self.assertEqual(res.status_code, 400)

    def testUserLogin(self):
        """
        Test a simple login success
        """
        res = self.client.post(self.login_url, self.login_data, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.json())

    def testUserLoginNoSuchUser(self):
        """
        Test a user cannot log in if the account does not exist
        """
        res = self.client.post(self.login_url, {
            "username": "nonExistentUser", "password": "Pass1234!"
        }, format="json")
        self.assertEqual(res.status_code, 404)

    def testUserLoginWithWrongPassword(self):
        """
        Test a user cannot log in with the wrong password
        """
        self.client.post(self.signup_url, self.user_data, format="json")  # Create user first
        res = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": "WrongPassword!"
        }, format="json")
        self.assertEqual(res.status_code, 401)

    def testUserLoginWithNoCredentials(self):
        """
        Test login fails with missing username or password
        """
        res = self.client.post(self.login_url, {}, format="json")
        self.assertEqual(res.status_code, 400)

    def testValidToken(self):
        """
        Test token authentication success
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        res = self.client.get(self.test_token_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("user", res.json())

    def testMissingToken(self):
        """
        Test request without token (should fail)
        """
        res = self.client.get(self.test_token_url)
        self.assertEqual(res.status_code, 403)

    def testInvalidToken(self):
        """
        Test request with an invalid token (should fail)
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token InvalidToken123")
        res = self.client.get(self.test_token_url)
        self.assertEqual(res.status_code, 403)

    def testUserLogout(self):
        """
        Test user can log out successfully
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        res = self.client.post(self.logout_url)
        self.assertEqual(res.status_code, 204)

    def testAccessProtectedRouteWithoutLogin(self):
        """
        Test accessing a protected route without authentication should fail
        """
        res = self.client.get(self.test_token_url)
        self.assertEqual(res.status_code, 403)

    def testAccessProtectedRouteAfterLogin(self):
        """
        Test accessing a protected route after login should succeed
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        res = self.client.get(self.test_token_url)
        self.assertEqual(res.status_code, 200)
