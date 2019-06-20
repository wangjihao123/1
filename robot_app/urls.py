from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home),
    path('upload_audio/', views.upload)
]


