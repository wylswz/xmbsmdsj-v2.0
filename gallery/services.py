from .utils import image_compress
from patent.settings import GALLERY_META
from .models import Photo

import logging
import os
import json

logger = logging.getLogger(__name__)


class ImageService:

    _metas: 'List[]' = None

    @classmethod
    def read_image_meta(cls) -> 'List[Photo]':
        if cls._metas is not None:
            return cls._metas
        res = []
        with open(GALLERY_META) as fp:
            img_dicts = json.load(fp)
            res = [
                Photo(**i) for i in img_dicts
            ]
        # This is one-shot caching.
        # Server restart is required when new photos are added
        cls._metas = res
        return res


    @classmethod
    def load_image_metas(cls, start=0, number=100):
        image_metas = cls.read_image_meta()[start: start+number]
        for image_meta in image_metas:
            thumbnail = image_meta.file_to_thumbnail()
            print(thumbnail)
            if not os.path.isfile(thumbnail):
                logger.info("Thumbnail: %s does not exist, creating", thumbnail)
                image_compress(image_meta.file_path, thumbnail)
        return image_metas