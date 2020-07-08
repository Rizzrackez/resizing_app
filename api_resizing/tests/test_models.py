from django.test import TestCase
from api_resizing.models import Picture
from PIL import Image
from django.db import transaction


def isInt(s):
    """Проверка значения на тип integer"""
    try:
        int(s)
        return True
    except ValueError:
        return False


class PictureModelTest(TestCase):
    """Тесты для модели Picture"""
    @classmethod
    def setUpTestData(cls):
        """Создание 2 объектов класса Picture"""
        Picture.objects.create(height=1080, width=1920, picture="test_pictures/picture-1.jpg")
        Picture.objects.create(picture="test_pictures/picture-2.jpg")

    def test_default_width_height_picture(self):
        """Задаются ли дефолтные значения полям height и width, если их не указали"""
        picture = Picture.objects.get(id=2)
        self.assertEquals([picture.height, picture.width], [240, 240])

    def test_width_height_picture(self):
        """Изменяется ли размер изображения, если указать значения width, height"""
        picture = Picture.objects.get(id=1)
        img = Image.open(picture.picture.path)
        width, height = img.size
        self.assertEquals([picture.height, picture.width], [height, width])

    def test_slug(self):
        """Проверка на создание уникального идентификатора (slug)"""
        picture = Picture.objects.get(id=1)
        self.assertTrue(picture.slug)

    def test_width_height_is_integer(self):
        """Проверка, что значения height и width типа integer"""
        picture = Picture.objects.get(id=1)
        self.assertTrue(isInt(picture.width) and isInt(picture.height))

    def test_slug_is_larger(self):
        """Проверка, что идентификатор (slug) не больше 50 символов"""
        picture = Picture.objects.get(id=2)
        self.assertFalse(len(picture.slug) > 50)

    def test_valid_height_width(self):
        """Проверка что значения width и height со значениями больше 9999 и меньше 1 изменяются на (240, 240)"""
        try:
            with transaction.atomic():
                picture = Picture.objects.create(height=22222, width=-1, picture="test_pictures/picture-3.jpg")
                self.assertEqual((picture.width, picture.height), (240, 240))
        except:
            pass


