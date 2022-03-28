from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('course/', views.allInfo),
    url(r'^showInfo', views.selectInfo, name='selectInfo')
]