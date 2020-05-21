from django.urls import path
import customers.views

urlpatterns = [
    path('profile/view', customers.views.view_profile, name='cust_view_profile'),
    path('profile/create', customers.views.create_profile, name='cust_create_profile'),
    path('profile/update', customers.views.update_profile, name='cust_update_profile'),
    ]
