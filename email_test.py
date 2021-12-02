from mail_sender.mail_sender import send_email_tareas
from sqs_service.sqs_service import sendMessageToQueue


send_email_tareas()
sendMessageToQueue(12)
