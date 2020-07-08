from django.urls import reverse
from rest_framework.test import APITestCase
from api_resizing.models import Picture
from django.test.client import RequestFactory
from api_resizing.views import PictureDetailView
from rest_framework import status
import json


class PictureViewTests(APITestCase):
    """Проверка поведения отображения. Корректных ответов сервера"""
    def setUp(self):
        self.picture = Picture.objects.create(height=1200, width=1300, picture='test_pictures/picture-2.jpg')
        self.picture_2 = Picture.objects.create(height=200, width=300, picture='test_pictures/picture-1.jpg')

    def test_list_view_status(self):
        """Проверка на возврат корректного HTTP статуса в случаи успешного запроса"""
        response = self.client.get(reverse('picture_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_view_data(self):
        """Проверка что данные со страницы 'api/v1/picture/list/' возвращаются в корректном виде"""
        request = self.client.get(reverse('picture_list'))

        picture_data = \
            [
                {
                    "slug": self.picture.slug,
                    "height": 1200,
                    "width": 1300,
                    "picture": "http://testserver/media/test_pictures/picture-2.jpg"
                },
                {
                    "slug": self.picture_2.slug,
                    "height": 200,
                    "width": 300,
                    "picture": "http://testserver/media/test_pictures/picture-1.jpg"
                }
            ]
        self.assertEqual(json.dumps(request.data), json.dumps(picture_data))

    def test_detail_view_and_status(self):
        """Успешно ли выполнен запрос к ресурсу 'api/v1/picture/<slug>/'. Проверка на возврат данных"""
        factory = RequestFactory()
        view = PictureDetailView.as_view()
        request = factory.get(f'api/v1/picture/detail/{self.picture.slug}/')
        response = view(request, slug=self.picture.slug)
        response.render()
        self.assertEqual(response.content, b'{"height":1200,'
                                           b'"width":1300,'
                                           b'"picture":"http://testserver/media/test_pictures/picture-2.jpg"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_view_and_status(self):
        """Создается ли объект по пути 'api/v1/picture/create/' методом post и успешно ли выполнен запрос"""
        with open('media/test_pictures/picture-1.jpg', 'rb') as img:
            pictures = img
            data = {'height': 1080, 'width': 1920, 'picture': pictures}
            response = self.client.post(reverse('picture_create'), data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Picture.objects.get(height=1080))

    def test_nonexistent_page(self):
        """Проверка на возврат корректного HTTP статуса в случаи, когда сервер не может найти запрошенный ресурс"""
        response = self.client.get('incorrect/page/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        """Проверка на возврат корректного HTTP статуса в случаи, когда HTTP метод не поддерживается"""
        response = self.client.get(reverse('picture_create'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
