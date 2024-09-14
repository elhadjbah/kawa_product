import pika
import json
import logging

logger = logging.getLogger(__name__)

# Publier un message dans une queue RabbitMQ
def publish_to_queue(queue_name, message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        logger.debug("Connexion à RabbitMQ établie pour la publication")
        channel = connection.channel()

        # Déclarez la file d'attente
        channel.queue_declare(queue=queue_name, durable=True)

        # Envoyez le message dans la file
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2) 
        )
        logger.info(f"Message envoyé à la queue {queue_name}: {message}")
        connection.close()
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message à la queue {queue_name}: {str(e)}")

# Consommer des messages depuis une queue RabbitMQ
def consume_from_queue(queue_name, callback):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        logger.info("Connexion à RabbitMQ établie pour la consommation")
        channel = connection.channel()

        # Déclarez la file d'attente
        channel.queue_declare(queue=queue_name, durable=True)

        def on_message(ch, method, properties, body):
            message = json.loads(body)
            logger.info(f"Message reçu de la queue {queue_name}: {message}")
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Démarrer la consommation des messages
        channel.basic_consume(queue=queue_name, on_message_callback=on_message)
        logger.debug(f"Attente des messages dans la queue {queue_name}...")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Erreur lors de la consommation de la queue {queue_name}: {str(e)}")
