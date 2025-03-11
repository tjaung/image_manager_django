from .test_setup import TestSetup
import pdb

class TestViews(TestSetup):

    def testUserSignup(self):
        """
        Test user sign up successfully
        """
        res = self.client.post(self.signup_url, 
                               self.user_data,
                               format="json")
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)

    def testUserCantSignupWithNoData(self):
        """
        Test that user can not sign up with incomplete data
        """
        res = self.client.post(self.signup_url)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 400)

    def testUserLogin(self):
        """
        Test a simple login success
        """
        res = self.client.post(self.login_url, 
                      self.login_data)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 200)

    def testUserLoginNoSuchUser(self):
        """
        Test a user can not login if there is no such account
        """

        res = self.client.post(self.login_url,
                               {"username": "mike",
                                "password": "Pass1234!"},
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
        self.assertIn("message", res.json())
        self.assertIn("user", res.json())

    def testMissingToken(self):
        """
        Test request without token (should fail)
        """

        res = self.client.get(self.test_token_url)
        # pdb.set_trace()
        self.assertEqual(res.status_code, 403)