

from sqs_service.sqs_service import sendMessageToQueue, deleteMessageOfQueue, getMessageOfQueue


def testSend():
    sendMessageToQueue(12)


def testGet():
    response = getMessageOfQueue()
    if response == None:
        print('No hay mensajes en la cola para procesar')
    else:
        print(response['taskId'])
        print(response['ReceiptHandle'])
        deleteMessageOfQueue(response['ReceiptHandle'])
        print('Mensaje borrado')


testSend()
