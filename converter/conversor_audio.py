from warnings import catch_warnings
import os

from ..constants import UPLOAD_FOLDER

OUT_PATH = UPLOAD_FOLDER
IN_PATH = UPLOAD_FOLDER


def convert_audio_os(filecode, out_extension):
    input_file = IN_PATH+filecode
    filename = "new-" + filecode.rsplit('.', 1)[0].lower()+"."+out_extension
    output_file = OUT_PATH+filename
    script = "ffmpeg -y -i " + input_file+" "+output_file
    os.system(script)
    return filename
