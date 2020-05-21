from django.urls import path
import customers.views

urlpatterns = [
    path('create_profile', customers.views.create_profile, name='create_profile'),
    ]
