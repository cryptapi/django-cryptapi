from django.urls import include, path
from cryptapi import views

app_name = 'cryptapi'

urlpatterns = [
    path('callback/', views.callback, name='callback'),
    path('status/', views.status, name='status'),
]
