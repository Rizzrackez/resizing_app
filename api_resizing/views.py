from rest_framework import generics
from api_resizing.models import Picture
from api_resizing.serializers import PictureCreateSerializer, PictureListSerializer, PictureDetailSerializer
from api_resizing.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status


class PictureCreateView(generics.CreateAPIView):
    serializer_class = PictureCreateSerializer


class PictureListView(generics.ListAPIView):
    serializer_class = PictureListSerializer
    queryset = Picture.objects.all()


class PictureDetailView(APIView):
    """
    Если переданный slug соответствует одному из объектов модели Picture, возвращает этот сериализованный объект.
    Если такого объекта нет, возвращает статус код - HTTP 404 Not Found. И тело - {"detail": "Not found."}
    """
    def get_object(self, slug):
        try:
            return Picture.objects.get(slug=slug)
        except:
            raise Http404

    def get(self, request, slug):
        picture = self.get_object(slug)
        serializer = PictureDetailSerializer(picture, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
