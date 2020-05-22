from django.urls import path
import photographers.views

urlpatterns = [
    # path('profile/view', photographers.views.view_profile, name='photographer_view_profile'),
    path('profile/create', photographers.views.create_profile, name='photographer_create_profile'),
    # path('profile/update', photographers.views.update_profile, name='photographer_update_profile'),
    path('profile/avatar', photographers.views.upload_avatar, name="upload_avatar"),
    path('profile/setnull', photographers.views.set_profile_img_to_null)
    ]
