from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='main'),
    path('add_new', views.AddNewImageView.as_view(), name='add_image'),
    path('edit/<int:pk>', views.EditImageView.as_view(), name='edit_image'),
]
