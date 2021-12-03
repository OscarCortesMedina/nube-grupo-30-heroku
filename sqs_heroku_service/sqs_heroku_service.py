import uuid
import pika
from constants import QUEUE_URL


QUEUE_NAME = 'TASK'
params = pika.URLParameters(QUEUE_URL)


def getMessageOfQueue(callback):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print("Received " + str(body))

    channel.basic_consume(QUEUE_NAME,
                          callback,
                          auto_ack=True)
    channel.start_consuming()
    connection.close()


def sendMessageToQueue(taskId):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue=QUEUE_NAME)  # Declare a queue
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=str(taskId))
    connection.close()
