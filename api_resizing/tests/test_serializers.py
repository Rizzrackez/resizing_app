from django.test import TestCase
from api_resizing.models import Picture
from api_resizing.serializers import PictureCreateSerializer


class PictureSerializerTest(TestCase):
    """Тесты для сериализаторов"""
    def setUp(self):
        self.picture_attributes = {
            "height": 1080,
            "width": 1920,
            "picture": "test_pictures/picture-3.jpg"
        }
        self.serializer_attributes = {
            "height": 1080,
            "width": 1920,
            "picture": "/media/test_pictures/picture-3.jpg"
        }

        self.picture = Picture.objects.create(height=self.picture_attributes['height'],
                                              width=self.picture_attributes['width'],
                                              picture=self.picture_attributes['picture'])

    def test_contains_expected_fields(self):
        """Проверка что сериализатор задает правильные значния ключам"""
        data = PictureCreateSerializer(instance=self.picture).data
        self.assertEqual(set(data.keys()), {'height', 'width', 'picture'})

    def test_create_picture(self):
        """Проверка что сериализованные данные создаются корректно"""
        serializer_picture = PictureCreateSerializer(instance=self.picture)
        self.assertDictEqual(serializer_picture.data, self.serializer_attributes)

