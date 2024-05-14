from typing import List

from ninja_extra import (
    ModelConfig,
    ModelControllerBase,
    ModelSchemaConfig,
    api_controller,
    http_get
)
from products.models import Produit
from schemas.types import ProduitSchema
from services.produit_service import ProduitService


@api_controller('/produits', tags=['API Produits'])
class ProduitController(ModelControllerBase):
    model_config = ModelConfig(
        model=Produit,
        schema_config=ModelSchemaConfig()
    )

    def __init__(self, produit_service: ProduitService):
        self.produit_service = produit_service

    @http_get('', description="Liste des produits")
    def get_produits(self) -> List[ProduitSchema]:
        return self.produit_service.get_produits()

    @http_get('/{int:produit_id}', description="Récupération d'un produit")
    def get_produit(self, produit_id: int) -> ProduitSchema:
        return self.produit_service.get_produit(produit_id)
