from warnings import catch_warnings
import os
OUT_PATH = '/home/ubuntu/Proyecto-Grupo30-202120/files-handler/'
IN_PATH = '/home/ubuntu/Proyecto-Grupo30-202120/files-handler/'


def convert_audio_os(filecode, out_extension):
    input_file = IN_PATH+filecode
    filename= "new-" + filecode.rsplit('.', 1)[0].lower()+"."+out_extension
    output_file = OUT_PATH+filename
    script = "ffmpeg -y -i " + input_file+" "+output_file
    os.system(script)
    return filename
