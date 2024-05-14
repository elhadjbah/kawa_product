import logging
from typing import List

from django.conf import Settings
from django.db import transaction
from injector import inject
from products.models import Produit
from schemas.types import ProduitSchema, ProduitCreate

logger = logging.getLogger()


class ProduitService:

    def get_produits(self):
        pass

    def get_produit(self, produit_id: int):
        pass


class ProduitServiceImpl(ProduitService):
    @inject
    def __init__(self, settings: Settings):
        logger.info(f"===== Using ProduitService =======")
        self.settings = settings

    @transaction.atomic
    def get_produits(self) -> List[ProduitSchema]:
        return Produit.objects.all()

    @transaction.atomic
    def get_produit(self, produit_id: int):
        return Produit.objects.get(pk=produit_id)
