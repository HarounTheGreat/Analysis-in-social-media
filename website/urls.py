from django.urls import path 
from . import views

app_name='website'

urlpatterns = [
    path('index2', views.index,name='index'),
    path('new/', views.form_data, name='new'),
]
