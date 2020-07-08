from django.db import models
from PIL import Image
import time


def create_picture_slug(picture, width: int, height: int):
    """Создание уникального идентификатора"""
    if len(picture) < 20:
        slug = f'{time.time()}-{width}-{height}-{picture[:-4]}'
    else:
        slug = f'{time.time()}-{width}-{height}-{picture[-20:-4]}'
    return slug


class Picture(models.Model):
    """
     Модель Picture содержит 4 поля:
     slug - уникальный идентификатор, который передается в качестве параметра URL
     height, width - размер изображения, по умолчанию равны 240. Если одно из значений > 9999 или < 1, то становится 240
     picture - изображение
    """
    slug = models.SlugField(blank=True, unique=True)
    height = models.IntegerField(default=240)
    width = models.IntegerField(default=240)
    picture = models.ImageField(upload_to='resizing_pictures')

    def check_max_height_width(self):
        if self.width > 9999 or self.width < 1:
            self.width = 240
        if self.height > 9999 or self.height < 1:
            self.height = 240

    def save(self, *args, **kwargs):
        self.slug = create_picture_slug(str(self.picture), self.width, self.height)
        self.check_max_height_width()
        super().save(*args, **kwargs)

        picture = Image.open(self.picture.path)
        picture = picture.resize((self.width, self.height))
        picture.save(self.picture.path)

    def __str__(self):
        if self.slug != '':
            return str(self.slug)
        else:
            return str(self.picture)


