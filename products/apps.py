from django.apps import AppConfig
from threading import Thread
import logging

logger = logging.getLogger(__name__)

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    has_started_consumer = False 
     
    def ready(self):
        # Démarrer le consommateur RabbitMQ
        logger.info("Démarrage du consommateur RabbitMQ pour la validation des produits")

        def start_rabbitmq_consumer():
            # Importer ProduitController ici pour éviter les erreurs liées au registre des apps
            from controllers.produit_controller import ProduitController
            controller = ProduitController(produit_service=None)  # Injecter ou instancier le service produit si nécessaire
            controller.start_rabbitmq_consumer()

        # Démarrer l'écoute des messages dans un thread séparé
        thread = Thread(target=start_rabbitmq_consumer)
        thread.daemon = True
        thread.start()
