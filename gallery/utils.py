from typing import TYPE_CHECKING
import json
import os
import codecs
from PIL import Image



if TYPE_CHECKING:
    from typing import List



def remove_bytes(dict1):
    for k,v in dict1.items():
        if isinstance(v, bytes):
            try:
                dict1[k] = ''
            except:
                dict1[k] = ''
        elif isinstance(v, dict):
            remove_bytes(v)
        elif not isinstance(v, str):
            dict1[k] = str(v)


def image_compress(src_dir, tgt_dir):
    exif = {}
    try:
        i = Image.open(src_dir)
        i.resize((i.size[0]//2,i.size[1]//2),Image.ANTIALIAS)
        with open(tgt_dir, 'w+') as file_t:
            i.save(file_t)

    except Exception as e:
        print(e)
    return exif
