from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('search_by_tag/<tag_id>', views.search_by_tag, name='search_by_tag')
]
