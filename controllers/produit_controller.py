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
from services.produit_service import ProduitServiceImpl
from services.rabbitmq_service import publish_to_queue, consume_from_queue
from services.authentication import ApiKey
from threading import Thread
from products.exceptions import NotFoundException, BadRequestException
import logging

# Configuration des logs
logger = logging.getLogger(__name__)

@api_controller('/produits', tags=['API Produits'])
class ProduitController:

    def __init__(self, produit_service: ProduitServiceImpl):
        self.produit_service = produit_service

        # Démarrer l'écoute des messages RabbitMQ pour la validation des produits
        thread = Thread(target=self.start_rabbitmq_consumer)
        thread.daemon = True  # Le thread se termine lorsque le serveur se termine
        thread.start()

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
        try:
            return self.produit_service.update_produit(produit_id, produit)
        except Produit.DoesNotExist:
            raise NotFoundException()

    @http_delete("/{int:produit_id}", auth=ApiKey(),
                 description="Supprimer définitivement un produit existant à partir de son id")
    def delete_produit(self, produit_id: int) -> bool:
        try:
            return self.produit_service.delete_produit(produit_id)
        except Produit.DoesNotExist:
            raise NotFoundException()

    # Démarrer la consommation des messages RabbitMQ
    def start_rabbitmq_consumer(self):
        logger.info("Consommateur RabbitMQ démarré pour la queue product_validation_queue")
        consume_from_queue('product_validation_queue', self.validate_product_availability)

    # Valider la disponibilité du produit
    def validate_product_availability(self, message):
        product_id = message.get('product_id')
        requested_quantity = message.get('requested_quantity')
        logger.info(f"Validation du produit demandée pour ID {product_id} et quantité {requested_quantity}")

        try:
            produit = Produit.objects.get(pk=product_id)
            if produit.stock >= requested_quantity:
                response = {
                    'product_id': product_id,
                    'status': 'available',
                    'requested_quantity': requested_quantity,
                    'client_id': message.get('client_id'),
                    'prix_total': message.get('prix_total')
                }
                logger.info(f"Produit {product_id} disponible en stock.")
            else:
                response = {
                    'product_id': product_id,
                    'status': 'unavailable',
                    'requested_quantity': requested_quantity,
                    'client_id': message.get('client_id'),
                    'prix_total': message.get('prix_total')
                }
                logger.warning(f"Produit {product_id} non disponible. Stock insuffisant.")
            
            # Publier la réponse dans la queue de validation
            publish_to_queue('product_validation_response_queue', response)
        except Produit.DoesNotExist:
            # Créer une réponse indiquant que le produit n'existe pas
            response = {
                'product_id': product_id,
                'status': 'not_found',
                'requested_quantity': requested_quantity,
                'client_id': message.get('client_id'),
                'prix_total': message.get('prix_total')
            }
            # Publier la réponse dans la queue de validation
            publish_to_queue('product_validation_response_queue', response)
            
            logger.error(f"Produit avec ID {product_id} non trouvé")
