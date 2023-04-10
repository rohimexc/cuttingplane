from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    path('input_fungsi', views.input_fungsi, name='input-fungsi'),
    path('proses/<str:token>', views.proses, name='proses'),
]