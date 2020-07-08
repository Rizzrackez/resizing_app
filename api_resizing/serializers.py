from rest_framework import serializers
from api_resizing.models import Picture


class PictureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('height', 'width', 'picture')


class PictureListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('slug', 'height', 'width', 'picture')


class PictureDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture
        fields = ('height', 'width', 'picture',)
