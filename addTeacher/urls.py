from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.addHtml),
    # path('delete/', views.delete, name='delete')
    url(r'^delete/', views.delete, name='delete'),
    url(r'^inputFile/', views.inputFile, name='inputFile'),
    url(r'^updateT', views.updateT, name='updateT'),
    url(r'^updateOne', views.updateOne, name='updateOne'),
    url(r'^deleteOne', views.deleteOne, name='deleteOne'),
    url(r'^screen', views.screen, name='screen'),
    url(r'^addOne', views.addOne, name='addOne')
]