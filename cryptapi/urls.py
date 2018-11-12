from django.urls import path
from cryptapi import views

app_name = 'cryptapi'

urlpatterns = [
    path('callback/', views.callback, name='callback')
]
