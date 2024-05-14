import logging
from typing import List

from django.conf import Settings
from injector import inject
from products.models import Produit
from schemas.types import ProduitSchema, ProduitCreate

logger = logging.getLogger()


class ProduitService:

    def get_produits(self):
        pass


class ProduitServiceImpl(ProduitService):
    @inject
    def __init__(self, settings: Settings):
        logger.info(f"===== Using ProduitService =======")
        self.settings = settings

    def get_produits(self) -> List[ProduitSchema]:
        return Produit.objects.all()
