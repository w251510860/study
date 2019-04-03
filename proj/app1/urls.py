from django.conf.urls import include, url
from . import views

urlpatterns = [
    url('index/', views.index),
    url('signature/', views.create_signal),
]
