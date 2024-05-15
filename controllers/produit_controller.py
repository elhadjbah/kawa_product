from typing import List

from ninja_extra import (
    ModelConfig,
    ModelControllerBase,
    ModelSchemaConfig,
    api_controller,
    http_get,
    http_post,
    http_put
)
from products.models import Produit
from schemas.types import ProduitSchema, ProduitCreate, ProduitUpdate
from services.produit_service import ProduitService


@api_controller('/produits', tags=['API Produits'])
class ProduitController:
    # class ProduitController(ModelControllerBase):
    # model_config = ModelConfig(
    #     model=Produit,
    #     schema_config=ModelSchemaConfig()
    # )

    def __init__(self, produit_service: ProduitService):
        self.produit_service = produit_service
        self.service = produit_service

    @http_get('')
    def get_produits(self) -> List[ProduitSchema]:
        return self.produit_service.get_produits()

    @http_get('/{int:produit_id}')
    def get_produit(self, produit_id: int) -> ProduitSchema:
        return self.produit_service.get_produit(produit_id)

    @http_post('', response={201: ProduitSchema})
    def create_produit(self, produit: ProduitCreate) -> ProduitSchema:
        return self.produit_service.create_produit(produit)

    @http_put('/{int:produit_id}')
    def update_produit(self, produit_id: int, produit: ProduitUpdate) -> ProduitSchema:
        return self.produit_service.update_produit(produit_id, produit)
