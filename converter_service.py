from constants.constants import UPLOAD_FOLDER
from converter.conversor_audio import convert_audio_os
from converter_service.db_file_service import change_task_to_processed, search_file_to_convert
from s3_service import uploadFile, downloadFile
import os

from sqs_service.sqs_service import deleteMessageOfQueue, getMessageOfQueue


def fileConverterHandler(fileName, format):
    downloadFile(fileName)
    output_file = convert_audio_os(fileName, format)
    file = open(UPLOAD_FOLDER+output_file, 'rb')
    uploadFile(output_file, file)
    os.remove(UPLOAD_FOLDER+fileName)
    os.remove(UPLOAD_FOLDER+output_file)


def processTaskFromQueue():
    message = getMessageOfQueue()
    if message == None:
        print("No task to process")
    else:
        task = search_file_to_convert(message['taskId'])
        if task == None:
            print("No task to process")
        else:
            fileConverterHandler(task.filecode, task.newformat)
            change_task_to_processed(task.id)
            deleteMessageOfQueue(message['ReceiptHandle'])


processTaskFromQueue()
