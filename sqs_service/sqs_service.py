import boto3
import uuid

BUCKET = 's3-grupo-30'
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/141348617543/lista-tareas-grupo-30.fifo'
ATTRIBUTE_NAME = 'taskId'
client = boto3.client('sqs', region_name='us-east-1')


def getMessageOfQueue():
    response = client.receive_message(
        QueueUrl=QUEUE_URL, MessageAttributeNames=[ATTRIBUTE_NAME])
    try:
        message = response['Messages'][0]
        taskId = int(message['MessageAttributes']
                     [ATTRIBUTE_NAME]['StringValue'])
        return {'ReceiptHandle': message['ReceiptHandle'], 'taskId': taskId}
    except KeyError:
        return None


def deleteMessageOfQueue(ReceiptHandle):
    client.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=ReceiptHandle)


def sendMessageToQueue(taskId):
    client.send_message(
        MessageBody='Lista de mensajes de tareas de conversión',
        MessageAttributes={'taskId': {
            'StringValue': str(taskId), 'DataType': 'Number'}},
        MessageGroupId='grupo30',
        MessageDeduplicationId=str(uuid.uuid4()),
        QueueUrl=QUEUE_URL)
