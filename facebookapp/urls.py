from django.urls import path 
from . import views

app_name='facebookapp'

urlpatterns = [
    path('token/', views.get_token,name='get_token'),
    path('new/', views.form_data, name='form_data'),
    path('savetoken/', views.save_token, name='save_token'),
    path('updatetoken/', views.update_token, name='update_token'),
]
