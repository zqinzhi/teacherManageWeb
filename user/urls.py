from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView),
    path('loginView/', views.loginView),
    path('register.html', views.registerView, name='register'),
    path('setpassword.html', views.setpasswordView, name='setpassword'),
    path('logout.html', views.logoutView, name='logout'),
]
