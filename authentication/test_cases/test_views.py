from .test_setup import TestSetup
import pdb

class TestViews(TestSetup):

    def testUserSignup(self):
        """
        Test user can sign up successfully
        """
        res = self.client.post(self.signup_url, {
            "username":"newguy",
            "password":"Pass1234!"
        }, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 201)
        self.assertIn("token", res.json())

    def testUserCantSignupWithNoData(self):
        """
        Test that a user cannot sign up with incomplete data
        """
        res = self.client.post(self.signup_url, {}, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)

    def testUserLogin(self):
        """
        Test a simple login success
        """
        res = self.client.post(self.login_url, self.login_data, format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.json())

    def testUserLoginNoSuchUser(self):
        """
        Test a user cannot log in if the account does not exist
        """
        res = self.client.post(self.login_url, 
                               {"username": "nonExistentUser", "password": "Pass1234!"},
                               format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 404)

    def testValidToken(self):
        """
        Test token authentication success
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        res = self.client.get(self.test_token_url)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)
        self.assertIn("user", res.json())

    def testMissingToken(self):
        """
        Test request without token (should fail)
        """
        res = self.client.get(self.test_token_url)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 403)
