"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from user import views as userviews
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('', include('home.urls')),
    path('user/', include('user.urls')),
    path('website/', include('website.urls')),
    path('ytb/', include('ytb.urls')),
    path('facebookapp/', include('facebookapp.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('contactus/',views.contactus,name="contactus"),
    path('contact/',views.contactus1,name="contactus1"),
    path('login/',userviews.login_form,name="login_form"),
    path('logout/',userviews.logout_func,name="logout_func"),
    path('register/',userviews.register_form,name="register_form"),


    

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
