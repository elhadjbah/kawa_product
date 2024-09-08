import requests
from decouple import config
from django.test import TestCase, Client
from django.conf import settings
from products.models import Produit
from services.produit_service import ProduitServiceImpl
from controllers.produit_controller import ProduitController
from products.exceptions import NotFoundException, BadRequestException
from schemas.types import ProduitCreate, ProduitUpdate


class ProduitControllerTest(TestCase):
    def setUp(self):
        self.SUCCESS_PRODUCT_ID = 1
        self.ERROR_PRODUCT_ID = 10000
        self.API_BASE_URL = config('CUSTOMER_API_URL')
        self.produit_controller = ProduitController(ProduitServiceImpl(settings))
        self.client = Client()
        for i in range(1, 4):
            Produit.objects.create(nom=f"Produit {i}", description=f"Description produit {i}", prix=10 * i,
                                   stock=100 - (10 * i))
        self.new_user = {
            "nom": "epsi",
            "prenom": "test",
            "date_naissance": "1999/09/13",
            "email": "jix@epsi.com",
            "mot_de_passe": "jix@test.epsi",
            "adresse": "7 Avenue de Lombez, 31300"
        }
        self.user_id = None
        self.headers = {
            "x-access-token": self.get_auth_token()
        }

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

    def get_auth_token(self):
        self.user_id = self._create_user(self.new_user).json()['id']
        auth_token = self._login().json()['accessToken']
        return auth_token

    def test_get_produits_success(self):
        response = self.client.get("/api/produits")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    # def test_get_produit_success(self):
    #     response = self.client.get(f"/api/produits/{self.SUCCESS_PRODUCT_ID}")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), {
    #         'id': self.SUCCESS_PRODUCT_ID,
    #         "nom": f"Produit {self.SUCCESS_PRODUCT_ID}",
    #         "description": f"Description produit {self.SUCCESS_PRODUCT_ID}",
    #         "prix": 10 * self.SUCCESS_PRODUCT_ID,
    #         "stock": 100 - (10 * self.SUCCESS_PRODUCT_ID)
    #    })

    def test_get_produit_error(self):
        response = self.client.get(f"/api/produits/{self.ERROR_PRODUCT_ID}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not Found : La ressource demandée n'a pas été retrouvée"})

    def test_raise_get_produit(self):
        with self.assertRaises(NotFoundException):
            self.produit_controller.get_produit(self.ERROR_PRODUCT_ID)

    # def test_delete_produit_success(self):
    #     response = self.client.delete(f"/api/produits/{self.SUCCESS_PRODUCT_ID}", headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), True)

    def test_delete_produit_error(self):
        response = self.client.delete(f"/api/produits/{self.ERROR_PRODUCT_ID}", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not Found : La ressource demandée n'a pas été retrouvée"})

    def test_create_produit(self):
        produit_json = {"nom": "Produit X", "description": "Produit X desc", "prix": 15.0, "stock": 80}
        response = self.client.post("/api/produits", data=produit_json,
                                    content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": Produit.objects.count(), **produit_json})

    # def test_update_produit_success(self):
    #     produit_json = {"nom": "Produit X1", "description": "Produit X1 desc", "prix": 125.0, "stock": 50}
    #     response = self.client.put(f"/api/produits/{self.SUCCESS_PRODUCT_ID}", data=produit_json,
    #                                content_type="application/json", headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), {"id": self.SUCCESS_PRODUCT_ID, **produit_json})

    def test_update_raise_error(self):
        produit_updated = ProduitUpdate(
            **{"nom": "Produit X1", "description": "Produit X1 desc", "prix": 125.0, "stock": 50})
        with self.assertRaises(NotFoundException):
            self.produit_controller.update_produit(self.ERROR_PRODUCT_ID, produit_updated)
