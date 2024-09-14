import pika

RABBITMQ_URL = 'localhost'

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_URL))
    print("Connexion réussie à RabbitMQ")
    connection.close()
except Exception as e:
    print(f"Erreur de connexion à RabbitMQ: {e}")
