from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path


urlpatterns = [

    path('', views.home, name="home"),
    path("signup", views.SignUp.as_view(), name="signup"),
    path('projets', views.projets, name='projets'),
    path('<int:id_projet>/profile', views.profile, name='profile'),
    path('updateuser', views.updateuser, name='updateuser'),
    path('addproject', views.addproject, name='addproject'),

]
