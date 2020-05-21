from django.urls import path
import customers.views

urlpatterns = [
    path('profile', customers.views.view_profile, name="view_profile"),
    path('create_profile', customers.views.create_profile, name='create_profile'),
    ]
