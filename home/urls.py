from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index,name="index"),
    path('', views.index1,name="index1"),
    path('HowItWorks', views.HowItWorks,name="HowItWorks"),
    ]