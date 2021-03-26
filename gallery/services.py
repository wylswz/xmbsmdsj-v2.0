from .models import read_image_meta
from .utils import image_compress
from patent.settings import GALLERY_META

import logging
import os

logger = logging.getLogger(__name__)


class ImageService:

    @classmethod
    def load_image_metas(cls, start=0, number=100):
        image_metas = read_image_meta(GALLERY_META)[start: start+number]
        for image_meta in image_metas:
            thumbnail = image_meta.file_to_thumbnail()
            print(thumbnail)
            if not os.path.isfile(thumbnail):
                logger.info("Thumbnail: %s does not exist, creating", thumbnail)
                image_compress(image_meta.file_path, thumbnail)
        return image_metas