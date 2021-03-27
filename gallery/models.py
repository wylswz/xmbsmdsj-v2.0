import os
import json


from PIL import Image
from PIL.TiffImagePlugin import IFDRational
from PIL.Image import Image as ImageObj, Exif
from pydantic import BaseModel, BaseConfig, Field
from typing import List, TYPE_CHECKING

from .utils import remove_bytes

from patent.settings import MEDIA_ROOT, MEDIA_URL

_THUMB_NAIL_SUFFIX = '_thumbnail'


_APERTURE = 0x9202
_EXPOSURE = 0x829A

_ISO = 0x8832
_MODEL = 0x0110
_SOFTWARE = 0x0131
_SHUTTER = 0x9201
_ORIENTATION = 0x0112


def frac_to_float(f: IFDRational):
    if f is None:
        return '0.0'
    n = f.numerator
    d = f.denominator
    if d == 0:
        return '0.0'
    return n/d

def frac_disp(f: IFDRational):
    if f is None:
        return '0/0'
    n = f.numerator
    d = f.denominator
    return '{}/{}'.format(n, d)

class Photo(BaseModel):
    id: int
    title: str
    summary: str
    file: str
    tags: List[str]
    thumbnail: str
    author: str
    cache_exif: Exif = None

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
    def aperture(self):
        frac: IFDRational = self._exif_raw().get(_APERTURE, None)
        return frac_to_float(frac)

    @property
    def exposure(self):
        frac = self._exif_raw().get(_EXPOSURE, '0')
        return frac_disp(frac)

    @property
    def model(self):
        return self._exif_raw().get(_MODEL, 'UNKNOWN')

    @property
    def ISO(self):
        return self._exif_raw().get(_ISO, 200)

    @property
    def software(self):
        return self._exif_raw().get(_SOFTWARE, 'UNKNOWN')

    @property
    def orientation(self):
        return self._exif_raw().get(_ORIENTATION, None)

    def _exif_raw(self) -> Exif:
        if  self.cache_exif is not None:
            return self.cache_exif

        i: ImageObj = Image.open(self.file_path)
        _exif = i.getexif()
        self.cache_exif = _exif
        return _exif

    def file_to_thumbnail(self):
        splitted = self.file_path.split('.')
        return '.'.join(splitted[:-1]) + _THUMB_NAIL_SUFFIX + '.' + splitted[-1]

    def serialize(self):
        d = self.dict(exclude={'cache_exif'})
        d.update(
            {
                'thumbnail_url': self.thumbnail_url,
                'file_url': self.file_url,
                'aperture': self.aperture,
                'exposure': self.exposure,
                'software': self.software,
                'model': self.model,
                'ISO': self.ISO,
            }
        )
        print(d)
        return d

    class Config(BaseConfig):
        arbitrary_types_allowed = True

