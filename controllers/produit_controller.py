from typing import List

from ninja_extra import (
    api_controller,
    http_get,
    http_post,
    http_put,
    http_delete
)
from products.models import Produit
from schemas.types import ProduitSchema, ProduitCreate, ProduitUpdate
from services.produit_service import ProduitService
from services.authentication import ApiKey
from products.exceptions import NotFoundException, BadRequestException


@api_controller('/produits', tags=['API Produits'])
class ProduitController:
    # class ProduitController(ModelControllerBase):
    # model_config = ModelConfig(
    #     model=Produit,
    #     schema_config=ModelSchemaConfig()
    # )

    def __init__(self, produit_service: ProduitService):
        self.produit_service = produit_service

    @http_get('', description="Récupérer la liste des produits disponibles")
    def get_produits(self) -> List[ProduitSchema]:
        return self.produit_service.get_produits()

    @http_get('/{int:produit_id}', description="Récupérer un produit spécifique à partir de son id")
    def get_produit(self, produit_id: int) -> ProduitSchema:
        try:
            return self.produit_service.get_produit(produit_id)
        except Produit.DoesNotExist:
            raise NotFoundException()

    @http_post('', response={201: ProduitSchema}, auth=ApiKey(),
               description="Ajouter un nouveau produit à la liste de produits")
    def create_produit(self, produit: ProduitCreate) -> ProduitSchema:
        return self.produit_service.create_produit(produit)

    @http_put('/{int:produit_id}', auth=ApiKey(),
              description="Mettre à jour un produit existant à partir de son id")
    def update_produit(self, produit_id: int, produit: ProduitUpdate) -> ProduitSchema:
        _produit = None
        try:
            _produit = self.produit_service.update_produit(produit_id, produit)
        except NotFoundException:
            raise NotFoundException()
        return _produit

    @http_delete("/{int:produit_id}", auth=ApiKey(),
                 description="Supprimer définitivement un produit existant à partir de son id")
    def delete_produit(self, produit_id: int) -> bool:
        try:
            return self.produit_service.delete_produit(produit_id)
        except NotFoundException:
            raise NotFoundException()


