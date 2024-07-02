from django.test import TestCase
from django.conf import settings
from products.models import Produit
from services.produit_service import ProduitServiceImpl
from products.exceptions import NotFoundException, BadRequestException
from schemas.types import ProduitCreate, ProduitUpdate


class ProduitServiceTest(TestCase):
    def setUp(self):
        self.produit_service = ProduitServiceImpl(settings)
        self.produit_unique = Produit.objects.create(nom="Café pur", description="90% de caféïne", prix=5, stock=100)
        self.produit_json = {"nom": "Produit X", "description": "Produit X desc", "prix": 15, "stock": 80}
        for i in range(3):
            Produit.objects.create(nom=f"Produit {i}", description=f"Description produit {i}", prix=10 * i,
                                   stock=100 - (10 * i))

    def test_get_produit_success(self):
        produit = self.produit_service.get_produit(self.produit_unique.pk)
        self.assertEqual(produit, self.produit_unique)

    def test_get_produit_not_found(self):
        produit_inexistant = 10000
        with self.assertRaises(NotFoundException):
            self.produit_service.get_produit(produit_inexistant)

    def test_get_produits(self):
        produits = self.produit_service.get_produits()

        self.assertEqual(len(produits), 4)

        for produit in produits:
            self.assertIn(produit, produits)

    def test_get_produits_empty(self):
        Produit.objects.all().delete()

        produits = self.produit_service.get_produits()

        self.assertEqual(list(produits), [])

    def test_create_produit_success(self):
        new_produit = ProduitCreate(**self.produit_json)

        created_produit = self.produit_service.create_produit(new_produit)

        produit_in_db = Produit.objects.get(pk=created_produit.id)
        self.assertIsNotNone(produit_in_db)

        self.assertIsInstance(created_produit, Produit)

    def test_update_produit(self):
        produit_update = ProduitUpdate.from_orm(self.produit_unique)
        produit_update.nom = "Café pur Update"

        updated_produit = self.produit_service.update_produit(self.produit_unique.pk, produit_update)
        self.assertIsNotNone(updated_produit)
        self.assertIsInstance(updated_produit, Produit)
        self.assertEqual(produit_update.nom, updated_produit.nom)

    def test_update_produit_not_found(self):
        produit_id = 10000
        produit_dummy_json = self.produit_json
        produit_dummy = ProduitUpdate(**produit_dummy_json)
        with self.assertRaises(NotFoundException):
            self.produit_service.update_produit(produit_id, produit_dummy)

    def test_update_empty_produit(self):
        produit_dummy = ProduitUpdate(**{})
        with self.assertRaises(BadRequestException):
            self.produit_service.update_produit(self.produit_unique.pk, produit_dummy)

    def test_delete_produit(self):
        produit = Produit.objects.create(**self.produit_json)
        result = self.produit_service.delete_produit(produit.id)
        self.assertTrue(result)
        with self.assertRaises(NotFoundException):
            self.produit_service.get_produit(produit.id)

    def test_delete_produit_not_found(self):
        with self.assertRaises(NotFoundException):
            self.produit_service.delete_produit(10001)

    # def test_get_produits_interface(self):