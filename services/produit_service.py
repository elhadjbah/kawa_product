import logging
from typing import List

from django.conf import Settings
from django.db import transaction
from injector import inject
from products.models import Produit
from products.exceptions import BadRequestException, NotFoundException
from schemas.types import ProduitSchema, ProduitCreate, ProduitUpdate

logger = logging.getLogger()


class ProduitService:

    def get_produits(self):
        pass

    def get_produit(self, produit_id: int):
        pass

    def create_produit(self, produit: ProduitCreate) -> ProduitSchema:
        pass

    def update_produit(self, produit_id: int, produit: ProduitUpdate):
        pass

    def delete_produit(self, produit_id: int):
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
        try:
            produit = Produit.objects.get(pk=produit_id)
        except Produit.DoesNotExist:
            raise NotFoundException()
        return produit

    @transaction.atomic
    def create_produit(self, produit: ProduitCreate) -> ProduitSchema:
        return Produit.objects.create(**produit.dict())

    @transaction.atomic
    def create_produit(self, produit: ProduitCreate) -> ProduitSchema:
        return Produit.objects.create(**produit.dict())

    @transaction.atomic
    def update_produit(self, produit_id: int, produit: ProduitUpdate) -> ProduitSchema:
        produit_to_update = None
        try:
            produit_to_update = Produit.objects.get(pk=produit_id)
            if not produit.dict():
                raise BadRequestException()
            for attr, value in produit.dict().items():
                setattr(produit_to_update, attr, value)
            produit_to_update.save()
        except Produit.DoesNotExist:
            raise NotFoundException()
        return produit_to_update

