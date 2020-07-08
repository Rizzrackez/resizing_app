from django.urls import path
from api_resizing.views import PictureListView, PictureCreateView, PictureDetailView

urlpatterns = [
    path('picture/list/', PictureListView.as_view(), name='picture_list'),
    path('picture/create/', PictureCreateView.as_view(), name='picture_create'),
    path('picture/detail/<str:slug>/', PictureDetailView.as_view(), name='picture_detail'),
]
