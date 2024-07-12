from typing import Optional

from imgutils.data import load_image
from PIL import ImageChops

from .base import ProcessAction
from ..model import ImageItem


class ModeConvertAction(ProcessAction):
    def __init__(self, mode='RGB', force_background: Optional[str] = 'white', crop_extra_background: bool = False):
        self.mode = mode
        self.force_background = force_background
        self.crop_extra_background = crop_extra_background

    def process(self, item: ImageItem) -> ImageItem:
        image = load_image(item.image, mode=self.mode, force_background=self.force_background)
        if self.crop_extra_background:
            diff = ImageChops.difference(item.image, image)
            bbox = ImageChops.add(diff, diff, 2.0, -100).getbbox()
            if bbox:
                image = image.crop(bbox)
        return ImageItem(image, item.meta)
