from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('input/', views.index, name='input'),
    path('output/', views.output, name='output'),
    path('file_view/<str:filename>/', views.file_view, name='file')
]