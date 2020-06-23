from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('search', views.search, name='search'),
    path('search_by_tag/<tag_id>', views.search_by_tag, name='search_by_tag'),
    path('terms_of_use', views.terms_of_use, name='terms_of_use'),
    path('license_agreements', views.license_agreements, name='license_agreements'),
]
