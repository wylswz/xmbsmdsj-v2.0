from patent.settings import hash
from utils.models import Token
token = Token.get_token()
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from PIL import Image
import json






def token_auth(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        pswd = args[0].POST.get('password')
        try:
            if hash(pswd) != token:
                return Response({"status":"error","message":"Unauthorized operation"},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return f(*args, **kwds)
        except Exception as e:
            return Response({"status":"error","message":"Unauthorized operation"}, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


def remove_bytes(dict1):
    for k,v in dict1.items():
        if isinstance(v,bytes):

            try:
                dict1[k] = ''
                
            except:
                dict1[k] = ''
        elif isinstance(v,dict):
            remove_bytes(v)

def image_compress(src_dir, tgt_dir):
    exif = {}
    try:
        i = Image.open(src_dir)
        i.resize((i.size[0]//2,i.size[1]//2),Image.ANTIALIAS)
        i.save(tgt_dir)
        exif = dict(i._getexif().items())
        remove_bytes(exif)
        print(exif)
        exif = json.dumps(exif)
    except Exception as e:
        pass
    return exif