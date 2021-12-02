import boto3
from constants import BUCKET, UPLOAD_FOLDER


def uploadFile(filename, data):
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET).put_object(Key=filename, Body=data)


def downloadFile(filename):
    s3 = boto3.client('s3')
    s3.download_file(BUCKET, filename, UPLOAD_FOLDER+filename)


def deleteFile(filename):
    s3 = boto3.resource('s3')
    s3.Object(BUCKET, filename).delete()
