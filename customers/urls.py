from django.urls import path
import customers.views

urlpatterns = [
    path('profile/view', customers.views.view_profile, name='cust_view_profile'),
    path('profile/create', customers.views.create_profile, name='cust_create_profile'),
    path('profile/update', customers.views.update_profile, name='cust_update_profile'),
    path('downloads/', customers.views.view_download, name="view_downloads"),
    path('add_to_favourite/<photo_id>', customers.views.add_to_favourite, name="add_to_favourite"),
    path('favourites/', customers.views.view_favourites, name='view_favourites')
    ]
