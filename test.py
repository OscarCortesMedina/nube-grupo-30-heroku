


from s3_service.s3_service import downloadFile, getURLLocation, uploadFile



file = open('runtime.txt', 'rb')
#uploadFile('runtime.txt',file)
#print(getURLLocation())
downloadFile('1-20211203-122401.mp3')