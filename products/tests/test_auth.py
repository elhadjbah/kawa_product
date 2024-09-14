from decouple import config
import requests
from django.test import TestCase


class AuthTest(TestCase):

    def setUp(self):
        self.API_BASE_URL = config('CUSTOMER_API_URL')
        self.new_user = {
            "nom": "epsi",
            "prenom": "test",
            "date_naissance": "1999/09/13",
            "email": "jix@epsi.com",
            "mot_de_passe": "jix@test.epsi",
            "adresse": "7 Avenue de Lombez, 31300"
        }
        self.user_id = None

    def tearDown(self):
        response = requests.delete(
            f"{self.API_BASE_URL}/api/customers/{self.user_id}")

    def _create_user(self, new_user):
        response = requests.post(
            f"{self.API_BASE_URL}/api/customers",
            data=new_user
        )
        return response

    def _login(self):
        response = requests.post(
            f"{self.API_BASE_URL}/api/login",
            data={
                "email": self.new_user['email'],
                "mot_de_passe": self.new_user['mot_de_passe']
            }
        )
        return response

    def _verify_token(self, token=None):
        if token is None:
            # first create a new user
            self._create_user(self.new_user)
            # then try to connect
            response = self._login()
            auth_token = response.json()['accessToken']
        else:
            auth_token = token
        response = requests.get(
            f"{self.API_BASE_URL}/api/auth/verify-token",
            headers={
                "x-access-token": auth_token
            }
        )
        return response

    def test_create_user(self):
        response = self._create_user(self.new_user)
        self.assertEqual(response.status_code, 200)
        for key in self.new_user.keys():
            self.assertIn(key, response.json())
        self.user_id = response.json()['id']

    def test_login(self):
        # first create a new user
        self._create_user(self.new_user)
        # then try to connect
        response = self._login()
        # check the return schema
        self.assertEqual(response.status_code, 200)
        for key in ['id', 'email', 'accessToken']:
            self.assertIn(key, response.json())

    def test_verify_token(self):
        response = self._verify_token()
        self.assertEqual(response.status_code, 200)
        for key in ['message', 'userId']:
            self.assertIn(key, response.json())

    def test_wrong_token(self): # getting token
        response = self._verify_token(token="xhttfyavak")
        self.assertEqual(response.status_code, 401)
        self.assertIn('message', response.json())

#