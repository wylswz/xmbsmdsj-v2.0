from typing import TYPE_CHECKING
from PIL import Image



if TYPE_CHECKING:
    from typing import List


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
