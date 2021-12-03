from constants.constants import UPLOAD_FOLDER
from converter.conversor_audio import convert_audio_os
from converter_service.db_file_service import change_task_to_processed, search_file_to_convert
from s3_service import uploadFile, downloadFile
import os

from sqs_heroku_service.sqs_heroku_service import getMessageOfQueue


def fileConverterHandler(fileName, format):
    print("filename "+fileName)
    downloadFile(fileName)
    print("File downloadad "+format)
    output_file = convert_audio_os(fileName, format)
    print("Opening file "+UPLOAD_FOLDER+output_file)
    file = open(UPLOAD_FOLDER+output_file, 'rb')
    print("File opened "+output_file)
    uploadFile(output_file, file)
    print("Rm "+UPLOAD_FOLDER+fileName)
    os.remove(UPLOAD_FOLDER+fileName)
    print("Rm "+UPLOAD_FOLDER+output_file)
    os.remove(UPLOAD_FOLDER+output_file)


def processTaskFromQueue(ch, method, properties, body):
    print('incoming message '+str(body))
    task = search_file_to_convert(int(body))
    if task == None:
        print("No task to process")
    else:
        fileConverterHandler(task.filecode, task.newformat)
        change_task_to_processed(task.id)
    print("Task converted succedfully "+str(body))


getMessageOfQueue(processTaskFromQueue)
