import os
import json


from PIL import Image
from pydantic import BaseModel, BaseConfig
from typing import List

from .utils import remove_bytes

from patent.settings import MEDIA_ROOT, MEDIA_URL

_THUMB_NAIL_SUFFIX = '_thumbnail'


class Photo(BaseModel):
    id: int
    title: str
    summary: str
    file: str
    tags: List[str]
    thumbnail: str
    author: str


    @property
    def thumbnail_url(self):
        return os.path.join(MEDIA_URL, self.thumbnail)

    @property
    def thumbnail_path(self):
        return os.path.join(MEDIA_ROOT, self.thumbnail)

    @property
    def file_url(self):
        return os.path.join(MEDIA_URL, self.file)

    @property
    def file_path(self):
        return os.path.join(MEDIA_ROOT, self.file)

    @property
    def exif(self):
        i = Image.open(self.file_path)
        _exif = i._getexif()
        print("Exif: ", _exif)
        if _exif is None:
            return "{1:\"asd\"}"
        exif = dict(_exif.items())
        remove_bytes(exif)
        return json.dumps(exif)

    def file_to_thumbnail(self):
        splitted = self.file_path.split('.')
        return '.'.join(splitted[:-1]) + _THUMB_NAIL_SUFFIX + '.' + splitted[-1]

    def serialize(self):
        d = self.dict()
        d.update(
            {
                'thumbnail_url': self.thumbnail_url,
                'file_url': self.file_url,
                'exif': self.exif
            }
        )
        return d


def read_image_meta(file: str) -> 'List[Photo]':
    res = []
    with open(file) as fp:
        img_dicts = json.load(fp)
        res = [
            Photo(**i) for i in img_dicts
        ]
    return res